from django.shortcuts import render
from imager_images.models import Photo
from random import choice


def home_view(request):
    photos = Photo.objects.filter(published='PUBLIC').all()
    # import pdb; pdb.set_trace()
    if len(photos) > 0:
            rand_pick = choice(photos)
            pic_path = rand_pick.image.url
    else:
        pic_path = '/static/4_Ornitography_34.jpg'

    context = {
        'photos': pic_path
    }

    return render(request, 'generic/home.html', context)
