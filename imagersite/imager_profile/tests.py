from django.test import TestCase
from .models import User
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

    def test_profile_has_bio(self):
        one_user = User.objects.all()[0]
        self.assertIsNotNone(one_user.profile.bio)

    def test_profile_has_phone(self):
        one_user = User.objects.all()[0]
        self.assertIsNotNone(one_user.profile.phone)

    def test_profile_has_location(self):
        one_user = User.objects.all()[0]
        self.assertIsNotNone(one_user.profile.location)

    def test_profile_has_website(self):
        one_user = User.objects.all()[0]
        self.assertIsNotNone(one_user.profile.website)

    def test_profile_has_fee(self):
        one_user = User.objects.all()[0]
        self.assertIsNotNone(one_user.profile.fee)

    def test_profile_has_is_active(self):
        one_user = User.objects.all()[0]
        self.assertIsNotNone(one_user.profile.is_active)

    def test_profile_has_camera(self):
        one_user = User.objects.all()[0]
        self.assertIsNotNone(one_user.profile.camera)

    def test_profile_has_services(self):
        one_user = User.objects.all()[0]
        self.assertIsNotNone(one_user.profile.services)

    def test_profile_has_photostyles(self):
        one_user = User.objects.all()[0]
        self.assertIsNotNone(one_user.profile.photostyles)
