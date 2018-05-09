from django.urls import path
from .views import PhotoView, AlbumView, LibraryView
from .views import AlbumDetailView, PhotoDetailView

urlpatterns = [
    path('library/', LibraryView.as_view(), name='library'),
    path('albums/', AlbumView.as_view(), name='albums'),
    path('photos/', PhotoView.as_view(), name='photos'),
    path('albums/<int:pk>', AlbumDetailView.as_view(), name='album_detail'),
    path('photos/<int:id>', PhotoDetailView.as_view(), name='photo_detail'),
]
