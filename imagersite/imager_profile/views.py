from django.views.generic import DetailView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from imager_images.models import Album, Photo
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ImagerProfile
from .forms import ProfileEditForm


class ProfileView(DetailView):
    """Renders profile view."""
    template_name = 'imager_profile/profile.html'
    context_object_name = 'profile'
    slug_url_kwargs = 'username'
    slug_field = 'user__username'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('home')
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

        # import pdb; pdb.set_trace()
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Render edit profile view."""
    template_name = "imager_profile/profile_edit.html"
    model = ImagerProfile
    form_class = ProfileEditForm
    login_url = reverse_lazy('auth_login')
    success_url = reverse_lazy('profile')
    slug_url_kwarg = 'username'
    slug_field = 'user__username'

    def get(self, *args, **kwargs):
        self.kwargs['username'] = self.request.user.get_username()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.kwargs['username'] = self.request.user.get_username()
        return super().post(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'username': self.request.user.username})
        return kwargs

    def form_valid(self, form):
        form.instance.user.email = form.data['email']
        form.instance.user.first_name = form.data['first_name']
        form.instance.user.last_name = form.data['last_name']
        form.instance.user.save()
        return super().form_valid(form)
