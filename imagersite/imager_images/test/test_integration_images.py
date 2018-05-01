from django.test import TestCase
from imager_profile.models import User
from ..models import Album, Photo
from model_mommy import mommy
import tempfile
import factory


class TestLibraryRoutes(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCase, cls)

        for n in range(10):
            user = mommy.make(User)
            user.set_password('password')
            user.save()
            album = mommy.make(Album, user=user)
            mommy.make(
                Photo,
                album=album,
                image=tempfile.NamedTemporaryFile(suffix='.png').name)

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
        super(TestCase, cls)

    def test_200_status_on_authenticated_request_to_library(self):
        user = User.objects.first()

        self.client.force_login(user)
        response = self.client.get('/images/library/')
        self.client.logout()
        self.assertEqual(response.status_code, 200)
    
    def test_200_status_on_authenticated_repsonse_to_album(self):
        """Test 200 status on authenticated repsonse to album."""
        user = User.objects.first()
        album = Album.objects.first()
        self.client.force_login(user)
        response = self.client.get('/images/albums/{}'.format(album.id))
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_200_status_on_authenticated_repsonse_to_photo(self):
        """Test 200 status on authenticated repsonse to photo."""
        user = User.objects.first()
        photo = Photo.objects.first()
        self.client.force_login(user)
        response = self.client.get('/images/photos/{}'.format(photo.id))
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_302_status_on_unauthenticated_repsonse_to_album(self):
        """Test 302 status on authenticated repsonse to album."""
        response = self.client.get('/images/albums/')
        self.assertEqual(response.status_code, 302)

    def test_302_status_on_unauthenticated_repsonse_to_photo(self):
        """Test 302 status on authenticated repsonse to photo."""
        response = self.client.get('/images/photos/')
        self.assertEqual(response.status_code, 302)

    def test_404_for_a_bad_request_to_album(self):
        """Test 404 status on a bad request."""
        response = self.client.get('/images/albums/doesnotexist')
        self.assertEqual(response.status_code, 404)

