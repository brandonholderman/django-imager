from django.shortcuts import render, redirect, get_object_or_404
from .models import Photo, Album
from imager_profile.models import ImagerProfile
from django.views.generic import ListView


# def library_view(request, username=None):
#     """Render library view."""

#     if not request.user.is_authenticated:
#         return redirect('home')

#     profile = get_object_or_404(ImagerProfile,
#                                 user__username=request.user.username)

#     photos = Photo.objects.filter(published='PUBLIC').all()
#     albums = Album.objects.filter(published='PUBLIC').all()

#     context = {
#         'profile': profile,
#         'photos': photos,
#         'albums': albums,
#     }

#     return render(request, 'imager_images/library.html', context)

class LibraryView(ListView):
    template_name = 'imager_images/library.html'
    context_object_name = 'library'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')

        return super().get(*args, **kwargs)

    def get_queryset(self, **kwargs):
        photo_query = Photo.objects.filter(published='PUBLIC')
        album_query = Album.objects.filter(published='PUBLIC')
        profile_query = get_object_or_404(ImagerProfile, user__username=self.request.user.username)

        return [photo_query, album_query, profile_query]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = context['library'][0]
        context['albums'] = context['library'][1]
        context['profile'] = context['library'][2]

        return context


class PhotoView(ListView):
    """Render photo view."""
    template_name = 'imager_images/photos.html'
    context_object_name = 'photos'
    # queryset = Photo.objects.filter(published='PUBLIC')

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')
        
        return super().get(*args, **kwargs)
    
    def get_queryset(self):
        
        return Photo.objects.filter(published='PUBLIC')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        return context


class AlbumView(ListView):
    """Render album view."""
    template_name = 'imager_images/albums.html'
    context_object_name = 'albums'
    # queryset = album.objects.filter(published='PUBLIC')

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')
        
        return super().get(*args, **kwargs)
    
    def get_queryset(self):
        return Album.objects.filter(published='PUBLIC')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        return context


def album_detail_view(request, id=None):
    """Render album_detail view."""

    if not request.user.is_authenticated:
        return redirect('home')

    # if not id:
    #     return redirect('albums')

    album_single = Album.objects.filter(id=id).all()

    context = {
        'albums': album_single,
    }

    return render(request, 'imager_images/album_detail.html', context)


def photo_detail_view(request, id=None):
    """Render photo_detail view."""

    if not request.user.is_authenticated:
        return redirect('home')

    # if not id:
    #     return redirect('photos')

    photo_single = Photo.objects.filter(id=id).all()

    context = {
        'photos': photo_single,
    }

    return render(request, 'imager_images/photo_detail.html', context)
