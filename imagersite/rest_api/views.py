from rest_framework import generics
from .serlializers import PhotoSerializer
from imager_images.models import Photo


class PhotoListApi(generics.ListAPIView):
    """Docstring."""
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(album__user=self.request.user)
