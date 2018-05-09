from django.shortcuts import render, redirect, get_object_or_404
from .models import Photo, Album
from imager_profile.models import ImagerProfile
from django.views.generic import ListView, DetailView, CreateView
from .forms import PhotoForm


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


class AlbumDetailView(DetailView):
    """Render album detail view."""
    template_name = 'imager_images/album_detail.html'
    context_object_name = 'album'
    model = Album

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')
        
        return super().get(*args, **kwargs)


class PhotoDetailView(DetailView):
    """Render photo detail view."""
    template_name = 'imager_images/photo_detail.html'
    context_object_name = 'photo'
    pk_url_kwarg = 'id'
    model = Photo

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')

        return super().get(*args, **kwargs)


class PhotoCreateView(CreateView):
    template_name = 'imager_images/photo_create.html'
    model = Photo
    form_class = PhotoForm
    success_url = 'photo'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')

        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')

        return super().post(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'username': self.request.user.username})
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# class AlbumCreateView(CreateView):
#     template_name = ''
#     model = Album
#     form_class = AlbumForm
#     success_url = 'album'

#     def get(self, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             return redirect('home')

#         return super().get(*args, **kwargs)

#     def post(self, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             return redirect('home')

#         return super().post(*args, **kwargs)

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs.update({'username': self.request.user.username})
#         return kwargs

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
