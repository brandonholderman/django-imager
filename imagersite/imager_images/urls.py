from django.urls import path
from .views import PhotoView, AlbumView, LibraryView
from .views import (AlbumDetailView, PhotoDetailView,
                    PhotoCreateView, AlbumCreateView,
                    PhotoEditView, AlbumEditView)

urlpatterns = [
    path('library/', LibraryView.as_view(), name='library'),
    path('albums/', AlbumView.as_view(), name='albums'),
    path('photos/', PhotoView.as_view(), name='photos'),
    path('photos/add', PhotoCreateView.as_view(), name='photo_create'),
    path('albums/add', AlbumCreateView.as_view(), name='album_create'),
    path('albums/<int:pk>', AlbumDetailView.as_view(), name='album_detail'),
    path('photos/<int:id>', PhotoDetailView.as_view(), name='photo_detail'),
    path('albums/<album_id>/edit/', AlbumEditView.as_view(), name='album_edit'),
    path('photos/<photo_id>/edit/', PhotoEditView.as_view(), name='photo_edit'),
]
