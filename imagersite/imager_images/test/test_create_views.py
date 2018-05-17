from django.test import TestCase, Client
from imager_profile.models import User
from ..models import Album, Photo
from model_mommy import mommy
import tempfile


class TestCreateRoutes(TestCase):
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


def test_200_status_on_authenticated_request_to_add_photo(self):
    """Test 200 status on aunthenticated response to add photo."""
    user = User.objects.first()
    self.client.force_login(user)
    response = self.client.get('/photos/add/')
    self.client.logout()
    self.assertEqual(response.status_code, 200)


def test_200_status_on_authenticated_request_to_add_album(self):
    """Test 200 status on aunthenticated response to add album."""
    user = User.objects.first()
    self.client.force_login(user)
    response = self.client.get('/albums/add/')
    self.client.logout()
    self.assertEqual(response.status_code, 200)
