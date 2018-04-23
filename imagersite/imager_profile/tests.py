from django.test import TestCase
from .models import ImagerProfile, User
import factory
import random

class UserFactory(factory.django.DjangoModelFactory):
    """ defines a mock user instance for testing """
    class Meta:
        model = User
    
    username = factory.Faker('user_name')
    email = factory.Faker('email')


class ProfileFactory(factory.django.DjangoModelFactory):
    """ defines a mock profile instance for testing """
    class Meta:
        model = ImagerProfile
    
    # bio = factory.Faker('')
    phone = factory.Faker('phone_number')
    # location = factory.Faker('')
    website = factory.Faker('domain_name')
    fee = round(random.uniform(0, 100), 2)
    is_active = factory.Faker('boolean')
    # camera = factory.Faker('')
    # services = factory.Faker('')
    # photostyles = factory.Faker('')


class ProfileUnitTests(TestCase):
    """ utlitizes the above classes to generate instances of
    user/profiles for use in testing
    """
    @classmethod
    def setUpClass(cls):
        super(TestCase, cls)
        for _ in range (50):
            user = UserFactory.create()
            user.set_password(factory.Faker('password'))
            user.save()

            profile = ProfileFactory.create(user=user)
            profile.save()
    
    @classmethod
    def tearDownClass(cls):
        super(TestCase, cls)
        User.objects.all().delete()
    
    def test_user_can_see_its_profle(self):
        one_user = User.objects.first()
        self.assertIsNotNone(one_user.profile)