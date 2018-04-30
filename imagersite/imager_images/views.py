from django.shortcuts import render, redirect, get_object_or_404
from .models import Photo, Album
from imager_profile.models import ImagerProfile


def library_view(request, username=None):
    """Render library view."""

    profile = get_object_or_404(ImagerProfile,
                                user__username=request.user.username)

    photos = Photo.objects.filter(published='PUBLIC').all()
    albums = Album.objects.filter(published='PUBLIC').all()

    context = {
        'profile': profile,
        'photos': photos,
        'albums': albums,
    }

    return render(request, 'imager_images/library.html', context)


def photo_view(request, username=None):
    """Render photo view."""

    photos = Photo.objects.filter(published='PUBLIC').all()

    context = {
        'photos': photos,
    }

    return render(request, 'imager_images/photos.html', context)


def album_view(request, username=None):
    """Render album view."""
    albums = Album.objects.filter(published='PUBLIC').all()

    context = {
        'albums': albums,
    }

    return render(request, 'imager_images/albums.html', context)


def album_detail_view(request, id=None):
    """Render album_detail view."""

    if not id:
        return redirect('albums')

    album_single = Album.objects.filter(id=id).all()

    context = {
        'albums': album_single,
    }

    return render(request, 'imager_images/album_detail.html', context)


def photo_detail_view(request, id=None):
    """Render photo_detail view."""
    # if not request.user.is_authenticated:
    #     return redirect('photos')

    if not id:
        return redirect('photos')

    photo_single = Photo.objects.filter(id=id).all()

    context = {
        'photos': photo_single,
    }

    return render(request, 'imager_images/photo_detail.html', context)
