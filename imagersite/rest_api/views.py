from rest_framework import generics, status
from .serlializers import PhotoSerializer, UserSerializer
from imager_images.models import Photo
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response


class PhotoListApi(generics.ListAPIView):
    """Docstring."""
    permission_classes = (IsAuthenticated,)
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(album__user=self.request.user)


class UserApi(generics.RetrieveAPIView, generics.CreateAPIView):
    """Docstring."""
    permission_classes = ''
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        if not pk:
            return Response(UserSerializer(
                request.user).data, status=status.HTTP_200_OK)
        return super().retrieve(request, pk)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
