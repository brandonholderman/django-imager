from django.forms import ModelForm
from .models import Photo


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'title', 'description', 'published']

    def __init__(self, *args, **kwargs):
        username = kwargs.pop('username')
        super().__init__(*args, **kwargs)
        self.fields['image'].queryset = Photo.objects.filter(
            album__user__username=username)
