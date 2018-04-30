from django.shortcuts import render
from imager_images.models import Photo
from random import choice


def home_view(request):
    """Renders home view"""
    photos = Photo.objects.filter(published='PUBLIC')
    # import pdb; pdb.set_trace()
    if len(photos) < 1:
        rand_pic = None
    else:
        rand_pic = choice(photos)

    context = {
        'photos': rand_pic
    }

    return render(request, 'generic/home.html', context)
