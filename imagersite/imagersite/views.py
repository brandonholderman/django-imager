from django.shortcuts import render
from imager_images.models import Photo
from random import choice


def home_view(request):
    photos = Photo.objects.filter(published='PUBLIC').all()
    # import pdb; pdb.set_trace()
    rand_pick = choice(photos)

    context = {
        'photos': rand_pick
    }

    return render(request, 'generic/home.html', context)
