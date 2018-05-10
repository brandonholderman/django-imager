from django.forms import ModelForm
from .models import Photo, Album


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'album', 'title', 'description', 'published']
        # import pdb; pdb.set_trace()

    def __init__(self, *args, **kwargs):
        username = kwargs.pop('username')
        super().__init__(*args, **kwargs)
        self.fields['album'].queryset = Album.objects.filter(
            user__username=username)


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['cover_image', 'name', 'description', 'published']
        # import pdb; pdb.set_trace()

    def __init__(self, *args, **kwargs):
        username = kwargs.pop('username')
        super().__init__(*args, **kwargs)
        self.fields['cover_image'].queryset = Photo.objects.filter(
            album__user__username=username)
