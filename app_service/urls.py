from django.urls import path

from .views import FileUploadView, MainPageView, FileDetailView


urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='upload-file'),
    path('', MainPageView.as_view(), name='main-page'),
    path('file/<int:file_id>/', FileDetailView.as_view(), name='file-detail'),
]
