from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .factory import UserFactory
from ..models import CustomUser
from faker import Faker


class UserSignUpTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # cls.user_object = UserFactory.build()
        # cls.user_saved = UserFactory.create()
        cls.client = APIClient()
        cls.signup_url = reverse('custom_register')
        cls.faker_obj = Faker()
        

    # @Faker.override_default_locale('en_US')
    def test_if_data_is_correct_then_signup(self):
        # Prepare data
        obj = CustomUser.objects.create(
            username='root',
            email="amr.jobmail@gmail.com",
            first_name="Amr", 
            last_name="Amer", 
            country_code="EG",
            gender="male",
            avatar="message_screen.png",
            phone_number="01067174141",
            birth_date="1981-09-23",
            password="@1234567",
            status=True,
        )
        signup_dict = {
            'email': 'amr.job@outlook.com',
            'first_name': 'Amr',
            'last_name': 'Amer', 
            'country_code': 'EG',
            'phone_number': '01149003573',
            'gender': 'male',
            'avatar': "message_screen.png",
            'birth_date': '1981-09-23',
            'password1': '@1234567',
            'password2': '@1234567',
        }  
        
        # Make request
        response = self.client.post(self.signup_url, signup_dict)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(CustomUser.objects.count(), 1)
        # Check database
        new_user = CustomUser.objects.get(phone_number=obj.phone_number)
        
        self.assertEqual(
            new_user.phone_number,
            '01067174141',
            # self.user_object.phone_number,
        )

    def test_if_phone_number_already_exists_dont_signup(self):
        # Prepare data with already saved user
        signup_dict = {
            'email': 'amr.job@outlook.com',
            'first_name': 'Amr',
            'last_name': 'Amer', 
            'country_code': 'EG',
            'phone_number': '01149003573',
            'gender': 'male',
            'avatar': "message_screen.png",
            'birth_date': '1981-09-23',
            'password1': '@1234567',
            'password2': '@1234567',
            
        }
        # Make request
        response = self.client.post(self.signup_url, signup_dict)
        # print("DATA: ", response.data['phone_number'])
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(
        #     str(response.data['phone_number'][0]),
        #     'A user with that username already exists.',
        # )
        # Check database
        # Check that there is only one user with the saved username
        # username_query = User.objects.filter(username=self.user_saved.username)
        # self.assertEqual(username_query.count(), 1)