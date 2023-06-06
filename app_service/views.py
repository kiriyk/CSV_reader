import csv
import re
import pandas as pd

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views import generic

from .forms import FileUploadForm
from .models import CSVFile


class MainPageView(generic.TemplateView):
    """
    Представление главной страницы
    """
    template_name = 'app_service/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        files = CSVFile.objects.all()
        context_list = []

        for file in files:
            context_list.append({
                'id': file.id,
                'file_name': file.file.name[10:-4],
                'columns': self.get_csv_columns(file.file.path)
            })

        context['files'] = context_list

        return context

    def get_csv_columns(self, file_path):
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            columns = next(csv_reader)

        return columns


class FileUploadView(LoginRequiredMixin, generic.FormView):
    """
    Представление загрузки нового файла
    """
    form_class = FileUploadForm
    template_name = 'app_service/upload.html'
    success_url = reverse_lazy('main-page')
    login_url = reverse_lazy('login-user')

    def form_valid(self, form):
        file = form.cleaned_data.get('file')
        obj = CSVFile(file=file, user=self.request.user)
        obj.save()
        return super().form_valid(form)


class FileDetailView(generic.DetailView):
    """
    Детальное представление файла
    """
    model = CSVFile
    template_name = 'app_service/detail.html'
    context_object_name = 'file'
    pk_url_kwarg = 'file_id'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file = context['file']
        df = pd.read_csv(file.file.path)

        filter_column = self.request.GET.get('filter_column') if self.request.GET.get('filter_column') else ''
        filter_value = self.request.GET.get('filter_value') if self.request.GET.get('filter_value') else ''
        sort_columns = self.request.GET.get('sort_columns') if self.request.GET.get('sort_columns') else []
        sort_orders = self.request.GET.get('sort_orders') if self.request.GET.get('sort_orders') else []
        query_string = self.get_query_string()

        df = self.get_sort_query(file, sort_columns, sort_orders, filter_column, filter_value, df)

        paginator = Paginator(df, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['filter_column'] = filter_column
        context['filter_value'] = str(filter_value)
        context['file_id'] = file.id
        context['sort_params'] = query_string if query_string else ''
        context['data'] = df
        context['sort_orders_dict'] = {column: order for column, order in zip(sort_columns, sort_orders)}

        return context

    def get_query_string(self):
        pattern_search = r'\?(.*)'
        pattern_modify = r'&?page=\d+'
        query_string = re.search(pattern_search, self.request.get_full_path())
        if query_string:
            query_string = '&' + query_string.group(1)
            query_string = re.sub(pattern_modify, '', query_string)

        return query_string

    def get_sort_query(self, file, sort_columns, sort_orders, filter_column, filter_value, df):
        if filter_value.isdigit():
            filter_value = float(filter_value)

        if filter_column and filter_value:
            df = df.loc[df[filter_column] == filter_value]

        sort_param = []
        for key, value in self.request.GET.items():
            if key.startswith('sort_param'):
                sort_param.append(value)

        sort_param = [param.split(',') for param in sort_param]
        for column, order in sort_param:
            sort_columns.append(column)
            sort_orders.append(order)

        if filter_column in sort_columns:
            idx = sort_columns.index(filter_column)
            sort_columns.remove(filter_column)
            sort_orders.pop(idx)

        sort_orders = [bool(sort_order) for sort_order in sort_orders]
        filtered_df = df.sort_values(by=sort_columns, ascending=sort_orders)

        return filtered_df


