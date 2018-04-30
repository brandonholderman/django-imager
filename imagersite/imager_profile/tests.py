from django.test import TestCase
from .models import ImagerProfile, User
from faker import Faker
import factory
import random


class UserFactory(factory.django.DjangoModelFactory):
    """ defines a mock user instance for testing """
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
    utlitizes the above classes to generate instances of
    user/profiles for use in testing
    """
    @classmethod
    def setUpClass(cls):
        super(TestCase, cls)
        for _ in range(50):
            user = UserFactory.create()
            user.set_password(factory.Faker('password'))
            user.save()

            # import pdb; pdb.set_trace()
            # populate_profile(user)
            # user.profile.save()

    @classmethod
    def tearDownClass(cls):
        super(TestCase, cls)
        User.objects.all().delete()

    def test_user_can_see_its_profle(self):
        one_user = User.objects.first()
        self.assertIsNotNone(one_user.profile)
