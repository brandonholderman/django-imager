from django.shortcuts import render, redirect, get_object_or_404
from imager_images.models import Album, Photo
from .models import ImagerProfile
from django.views.generic import DetailView


class ProfileView(DetailView):
    template_name = 'imager_profile/profile.html'
    context_object_name = 'profile'
    slug_url_kwargs = 'username'
    slug_field = 'user__username'
    # queryset = ImagerProfile.objects.filter(user__username=slug_field)
    # queryset = get_object_or_404(ImagerProfile, user__username='username')

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')
        # import pdb; pdb.set_trace()
        if self.kwargs == {}:
            self.kwargs['username'] = self.request.user.get_username()

        return super().get(*args, **kwargs)

    def get_object(self):
        return ImagerProfile.objects.filter(user__username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = context['object'][0].user.username
        profile = get_object_or_404(ImagerProfile, user__username=username)
        albums = Album.objects.filter(user__username=username)
        photos = Photo.objects.filter(album__user__username=username)

        context = {
            'profile': profile,
            'albums': albums,
            'photos': photos
            }

        return context



# class ProfileView(TemplateView)


# def profile_view(request, username=None):
#     """Renders profile view"""
#     owner = False

#     if not username:
#         username = request.user.get_username()
#         owner = True
#         if username == '':
#             return redirect('home')

#     profile = get_object_or_404(ImagerProfile, user__username=username)
#     albums = Album.objects.filter(user__username=username)
#     photos = Photo.objects.filter(album__user__username=username)

#     if not owner:
#         photos = Photo.objects.filter(published='PUBLIC')
#         albums = Album.objects.filter(published='PUBLIC')

#     context = {
#         'profile': profile,
#         'albums': albums,
#         'photos': photos
#     }

#     return render(request, 'imager_profile/profile.html', context)