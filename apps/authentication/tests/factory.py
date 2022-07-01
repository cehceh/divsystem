## https://www.rootstrap.com/blog/testing-in-django-django-rest-basics-useful-tools-good-practices/

from faker import Faker as FakerClass
from faker import config, providers
import faker
from typing import Any, Sequence
from factory import django, Faker, post_generation

from ..models import CustomUser

# config.DEFAULT_LOCALE = 'en_US'
# FakerClass._DEFAULT_LOCALE = 'en_US'
# CATEGORIES_VALUES = [x[0] for x in Category.choices]
# from faker.providers import BaseProvider

FakerClass._DEFAULT_LOCALE = 'en_US'

def fake(name):
    return FakerClass(name).generate({})

def faker():
    return FakerClass._get_faker()

# class MyProvider(BaseProvider):
#     def category_name(self):
#         return self.random_element(category_names)
#     ...
# factory.Faker.add_provider(MyProvider)


# class MyProvider(providers.BaseProvider):
#     def smth(self):
#         return self.random_element([1, 2, 3])

# FakerClass.add_provider(MyProvider)



class UserFactory(django.DjangoModelFactory):

    class Meta:
        model = CustomUser
    
    username = Faker('user_name')
    phone_number = Faker('phone_number')
    email = Faker('email') #: 'amr.jobmail@gmail.com',
    first_name = Faker('first_name') #: 'Amr',
    last_name = Faker('last_name') #: 'Amer', 
    # country_code = Faker('country_code') #: 'EG',
    # gender = Faker('gender') #: 'male',
    # avatar = Faker('avatar') #: "",
    # birth_date = Faker('birth_date') #: '1981-09-23',
    password = Faker('password')  # : '@1234567',

    # category = Faker('random_element', elements=CATEGORIES_VALUES)

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else FakerClass().password(
                length=30,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            )
        )
        self.set_password(password)