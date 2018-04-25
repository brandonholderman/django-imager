from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField


# Create your models here.
class Album(models.Model):
    """Class starting properties of photo album"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='albums')
    cover_image = models.ForeignKey('Photo', on_delete=models.CASCADE,
                                    related_name='+', null=True, blank=True)
    name = models.CharField(max_length=180, default='Untitled')
    description = models.TextField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(blank=True, null=True)
    published = models.CharField(
        max_length=7,
        choices=(('PRIVATE', 'Private'),
                 ('SHARED', 'Shared'),
                 ('PUBLIC', 'Public')
                 )
    )

    def __str__(self):
        """ string method for class """
        return '{}'.format(self.name)


class Photo(models.Model):
    """Class starting properties of each photo"""
    album = models.ForeignKey(Album, on_delete=models.CASCADE,
                              related_name='photos')
    image = ImageField(upload_to='images')
    title = models.CharField(max_length=180, default='Untitled')
    description = models.TextField(blank=True, null=True)
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(blank=True, null=True)
    published = models.CharField(
        max_length=7,
        choices=(('PRIVATE', 'Private'),
                 ('SHARED', 'Shared'),
                 ('PUBLIC', 'Public')
                 )
    )

    def __str__(self):
        """ string method for class """
        return '{}'.format(self.title)
