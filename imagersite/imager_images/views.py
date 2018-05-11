from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import PhotoForm, AlbumForm, PhotoEditForm, AlbumEditForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from imager_profile.models import ImagerProfile
from django.urls import reverse_lazy
from .models import Photo, Album


class LibraryView(ListView):
    """Renders library view."""
    template_name = 'imager_images/library.html'
    context_object_name = 'library'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')

        return super().get(*args, **kwargs)

    def get_queryset(self, **kwargs):
        photo_query = Photo.objects.filter(published='PUBLIC').filter(
            album__user__username=self.request.user.username)
        album_query = Album.objects.filter(published='PUBLIC').filter(
            user__username=self.request.user.username)
        profile_query = get_object_or_404(
            ImagerProfile,
            user__username=self.request.user.username)

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
    """Render view to add photos."""
    template_name = 'imager_images/photo_create.html'
    model = Photo
    form_class = PhotoForm
    success_url = reverse_lazy('library')

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


class AlbumCreateView(CreateView):
    """Renders view to add albums."""
    template_name = 'imager_images/album_create.html'
    model = Album
    form_class = AlbumForm
    success_url = reverse_lazy('library')

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


class PhotoEditView(LoginRequiredMixin, UpdateView):
    """Renders view to edit photos."""
    template_name = "imager_images/photo_edit.html"
    model = Photo
    form_class = PhotoEditForm
    login_url = reverse_lazy('auth_login')
    success_url = reverse_lazy('photos')
    slug_url_kwarg = 'photo_id'
    slug_field = 'id'

    def get(self, *args, **kwargs):
        self.kwargs['username'] = self.request.user.get_username()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.kwargs['username'] = self.request.user.get_username()
        return super().post(*args, **kwargs)

    def form_valid(self, form):
        form.instance.title = form.data['title']
        form.instance.save()
        return super().form_valid(form)


class AlbumEditView(LoginRequiredMixin, UpdateView):
    """Renders view to add albums."""
    template_name = "imager_images/album_edit.html"
    model = Album
    form_class = AlbumEditForm
    login_url = reverse_lazy('auth_login')
    success_url = reverse_lazy('albums')
    slug_url_kwarg = 'album_id'
    slug_field = 'id'

    def get(self, *args, **kwargs):
        self.kwargs['username'] = self.request.user.get_username()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.kwargs['username'] = self.request.user.get_username()
        return super().post(*args, **kwargs)

    def form_valid(self, form):
        form.instance.name = form.data['name']
        form.instance.save()
        return super().form_valid(form)
