# from django.contrib.auth.models import AnonymousUser
# from django.http import Http404
from django.test import TestCase, RequestFactory
from .models import ImagerProfile, User
from django.urls import reverse_lazy
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


class ProfileRouteTests(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        user_one = UserFactory(username='brandon',
                               email='brandon@brandon.brandon')
        user_one.set_password('password')
        user_one.save()

        populate_profile(user_one)
        user_one.profile.save()

        user_two = UserFactory(username='tyler', email='tyler@tyler.tyler')
        user_two.set_password('password')
        user_two.save()

        populate_profile(user_two)
        user_two.profile.save()

        self.brandon = user_one
        self.tyler = user_two

    def tearDown(self):
        User.objects.all().delete()

    def test_profile_view_with_no_user_name_not_logged_in_redirets_home(self):
        response = self.client.get(reverse_lazy('profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_route_has_200_response_given_an_authenticated_user(self):
        c = Client()
        c.login(username=self.brandon.username, password='password')
        response = c.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_profile_route_has_user_info(self):
        c = Client()
        c.login(username=self.brandon.username, password='password')
        response = c.get('/profile/')
        self.assertEqual(
            response.context['user'].username, self.brandon.username)

    def test_profile_route_does_not_allow_editing_for_other_users(self):
        c = Client()
        c.login(username=self.brandon.username, password='password')
        response = c.get('/profile/tyler')
        self.assertNotIn(b'Edit Profile', response.content)

    # def test_profile_route_does_allow_editing_for_signed_in_users(self):
    #     c = Client()
    #     c.login(username=self.brandon.username, password='password')
    #     response = c.get('/profile/brandon')
    #     self.assertIn(b'Edit Profile', response.content)

    def test_profile_route_returns_302_if_user_does_not_exist(self):
        c = Client()
        response = c.get('/profile/does_not_exist')
        self.assertEqual(response.status_code, 302)

    def test_profile_route_redirects_if_not_logged_in(self):
        """Test profiel route redirects if not logged in."""
        c = Client()
        response = c.get('/profile/')
        self.assertEqual(response.status_code, 302)

    def test_active_class_method(self):
        """Test active class method."""
        all_active = ImagerProfile.active()
        self.assertIsNotNone(all_active)

    def test_str_method_on_username(self):
        """Test string method on album."""
        one_profile = ImagerProfile.objects.first()
        one_profile.user.username = 'tandon'
        self.assertEqual(str(one_profile), 'tandon')
