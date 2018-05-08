from django.urls import path
from .views import PhotoView, AlbumView, LibraryView
from .views import album_detail_view, photo_detail_view

urlpatterns = [
    path('library/', LibraryView.as_view(), name='library'),
    path('albums/', AlbumView.as_view(), name='albums'),
    path('photos/', PhotoView.as_view(), name='photos'),
    path('albums/<int:id>', album_detail_view, name='album_detail'),
    path('photos/<int:id>', photo_detail_view, name='photo_detail'),
]
