
from django.views.generic import TemplateView
from imager_images.models import Photo

class HomeView(TemplateView):
    template_name = 'generic/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photos = Photo.objects.filter(published='PUBLIC')

        if photos.count():
            image = photos.order_by('?').first()
            image_url = image.image.url
            image_title = image.title

        else:
            image = None
            image_url = 'http://via.placeholder.com/250x250'
            image_title = 'Placeholder'

        context['image'] = image
        context['image_url'] = image_url
        context['image_title'] = image_title
        # import pdb; pdb.set_trace()

        return context


# from django.shortcuts import render
# from random import choice

# def home_view(request):
#     """Renders home view"""
#     photos = Photo.objects.filter(published='PUBLIC')
#     # import pdb; pdb.set_trace()
#     if len(photos) < 1:
#         rand_pic = None
#     else:
#         rand_pic = choice(photos)

#     context = {
#         'photos': rand_pic
#     }

#     return render(request, 'generic/home.html', context)
