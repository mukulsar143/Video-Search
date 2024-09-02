# videos/views.py

from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Video, Subtitle
from .serializers import VideoSerializer, SubtitleSerializer
from .tasks import process_video

class VideoUploadView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        video = serializer.save()
        process_video.delay(video.id)
        return video

class SubtitleSearchView(generics.ListAPIView):
    serializer_class = SubtitleSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        return Subtitle.objects.filter(text__icontains=query)
