from django.urls import path
from .views import *

urlpatterns = [
    path('upload/', VideoUploadView.as_view(), name='video-upload'),
    path('search/', SubtitleSearchView.as_view(), name='video-search'),
]
