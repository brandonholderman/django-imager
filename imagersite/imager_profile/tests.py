from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from .models import ImagerProfile, User
from django.http import Http404

from django.test import Client
from faker import Faker
import factory
import random


class UserFactory(factory.django.DjangoModelFactory):
    """ Defines a mock user instance for testing """
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')


def populate_profile(user):
    """Create profile for user class."""
    fake = Faker()
    user.profile.bio = fake.sentence()
    user.profile.phone = fake.phone_number()
    user.profile.location = fake.state_abbr()
    user.profile.website = fake.domain_name()
    user.profile.fee = round(random.uniform(0, 100), 2)
    user.profile.is_active = fake.boolean()
    user.profile.camera = 'DSLR'
    user.profile.services = 'weddings'
    user.profile.photostyles = 'night'


class ProfileUnitTests(TestCase):
    """
    Utlitizes the above classes to generate instances of
    user/profiles for use in testing
    """
    @classmethod
    def setUpClass(cls):
        super(TestCase, cls)
        for _ in range(50):
            user = UserFactory.create()
            user.set_password(factory.Faker('password'))
            user.save()

            populate_profile(user)
            user.profile.save()

    @classmethod
    def tearDownClass(cls):
        super(TestCase, cls)
        User.objects.all().delete()

    def test_user_can_see_its_profle(self):
        """Test user can see profile."""
        one_user = User.objects.first()
        self.assertIsNotNone(one_user.profile)

    def test_user_can_point_to_its_profile(self):
        """Test user can point to it's profile."""
        one_user = User.objects.all()[0]
        self.assertIsNotNone(one_user.profile)

    # def test_profile_has_bio(self):
    #     one_user = User.objects.all()[0]
    #     self.assertIsNotNone(one_user.profile.bio)

    # def test_profile_has_phone(self):
    #     one_user = User.objects.all()[0]
    #     self.assertIsNotNone(one_user.profile.phone)

    # def test_profile_has_location(self):
    #     one_user = User.objects.all()[0]
    #     self.assertIsNotNone(one_user.profile.location)

    # def test_profile_has_website(self):
    #     one_user = User.objects.all()[0]
    #     self.assertIsNotNone(one_user.profile.website)

    # def test_profile_has_fee(self):
    #     one_user = User.objects.all()[0]
    #     self.assertIsNotNone(one_user.profile.fee)

    # def test_profile_has_is_active(self):
    #     one_user = User.objects.all()[0]
    #     self.assertIsNotNone(one_user.profile.is_active)

    # def test_profile_has_camera(self):
    #     one_user = User.objects.all()[0]
    #     self.assertIsNotNone(one_user.profile.camera)

    # def test_profile_has_services(self):
    #     one_user = User.objects.all()[0]
    #     self.assertIsNotNone(one_user.profile.services)

    # def test_profile_has_photostyles(self):
    #     one_user = User.objects.all()[0]
    #     self.assertIsNotNone(one_user.profile.photostyles)

    # def test_profile_is_created_when_user_is_updated(self):
    #     """Test profile created when user is updated."""
    #     self.assertEquals(ImagerProfile.objects.count(), 50)
    #     one_user = User.objects.last()
    #     one_user.username = 'TandonHolderbone'
    #     one_user.save()
    #     self.assertEquals(ImagerProfile.objects.count(), 50)

    # def test_all_items_in_active(self):
    #     """Test that active method gets all active profiles."""
    #     one_user = User.objects.last()
    #     one_user.is_active = False
    #     one_user.save()

    #     active_profiles = ImagerProfile.active
    #     all_profiles = ImagerProfile.objects.all()
    #     self.assertEquals(active_profiles.count(), all_profiles.count() - 1)


class ProfileRouteTests(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        user_one = UserFactory(username='gandalf', email='wizard@middle.earth')
        user_one.set_password('password')
        user_one.save()

        populate_profile(user_one)
        user_one.profile.save()

        user_two = UserFactory(username='bilbo', email='hobbit@middle.earth')
        user_two.set_password('password')
        user_two.save()

        populate_profile(user_two)
        user_two.profile.save()

        self.gandalf = user_one
        self.bilbo = user_two

    def tearDown(self):
        User.objects.all().delete()

    def test_profile_view_shows_please_login_when_unauthenticated(self):
        from .views import profile_view
        request = self.request.get('/profile/')
        request.user = AnonymousUser()
        response = profile_view(request, 'gandalf')
        self.assertIn(b'Please log into the site', response.content)

    def test_profile_view_with_no_user_name_not_logged_in_redirets_home(self):
        from .views import profile_view
        request = self.request.get('/profile/')
        request.user = AnonymousUser()
        response = profile_view(request)
        self.assertEqual(response.status_code, 302)

    def test_profile_view_with_bad_user_returns_404(self):
        from .views import profile_view
        request = self.request.get('/profile/')
        request.user = AnonymousUser()
        with self.assertRaises(Http404):
            profile_view(request, 'Bilbo')

    def test_profile_route_has_200_response_given_an_authenticated_user(self):
        c = Client()
        c.login(username=self.gandalf.username, password='password')
        response = c.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_profile_route_has_user_info(self):
        c = Client()
        c.login(username=self.gandalf.username, password='password')
        response = c.get('/profile/')
        self.assertEqual(
            response.context['user'].username, self.gandalf.username)

    def test_profile_route_does_not_allow_editing_for_other_users(self):
        c = Client()
        c.login(username=self.gandalf.username, password='password')
        response = c.get('/profile/bilbo')
        self.assertNotIn(b'Edit Profile', response.content)

    # def test_profile_route_does_allow_editing_for_signed_in_users(self):
    #     c = Client()
    #     c.login(username=self.gandalf.username, password='password')
    #     response = c.get('/profile/gandalf')
    #     self.assertIn(b'Edit Profile', response.content)

    def test_profile_route_returns_404_if_user_does_not_exist(self):
        c = Client()
        response = c.get('/profile/does_not_exist')
        self.assertEqual(response.status_code, 404)

    def test_profile_route_redirects_if_not_logged_in(self):
        c = Client()
        response = c.get('/profile/')
        self.assertEqual(response.status_code, 302)
