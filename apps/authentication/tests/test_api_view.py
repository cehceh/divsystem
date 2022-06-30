from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from django.contrib.auth.hashers import make_password
from unittest.mock import patch

from ..models import CustomUser

from .factory import UserFactory

from faker import Faker

# Create your tests here.

class MyAPIViewTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_object = UserFactory.build()
        cls.user_saved = UserFactory.create()
        cls.client = APIClient()
        cls.signup_url = reverse('custom_register')
        # cls.faker_obj = Faker()

    def authenticate(self):
        self.client.post(
            reverse( 'custom_register'), {
                'email': 'amr.jobmail@gmail.com',
                'first_name': 'Amr',
                'last_name': 'Amer', 
                'country_code': 'EG',
                'phone_number': self.user_object.phone_number,#'01067174141',
                'gender': 'male',
                'avatar': "",
                'birth_date': '1981-09-23',
                'password': '@1234567',
            }                    
        )
        response = self.client.post(
            reverse( 'custom_login'), {
                'phone_number': '01067174141',
                'password': '@1234567',
            }
        )
        print('RESPONSE: ', response)
        # self.client.credentials(
        #     HTTP_AUTHORIZATION=f"Bearer {response.data['token']}"
        # )

    def test_if_data_is_correct_then_signup(self):
        # response = self.client.get(reverse( 'custom_register'), )
        signup_dict = {
            'email': 'amr.jobmail@gmail.com',
            'first_name': 'Amr',
            'last_name': 'Amer', 
            'country_code': 'EG',
            'phone_number': '01067174141',
            'gender': 'male',
            'avatar': "",
            'birth_date': '1981-09-23',
            'password1': '@1234567',
            'password2': '@1234567',
        }
        # )
        # Make request
        response = self.client.post(self.signup_url, signup_dict)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        # Check database
        new_user = CustomUser.objects.get(phone_number=self.user_object.phone_number)
        # self.assertEqual(
        #     new_user.category,
        #     self.user_object.category,
        # )
        self.assertEqual(
            new_user.phone_number,
            self.user_object.phone_number,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    # @patch.object(DisplayTranslation, "permission_classes", [])
    # def test_login_view(self):
    #     header = {'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.token)}
    #     obj = CustomUser.objects.create(
    #         username='root',
    #         email="amr.jobmail@gmail.com",
    #         first_name="Amr", 
    #         last_name="Amer", 
    #         country_code="EG",
    #         gender="male",
    #         phone_number="01067174141",
    #         password='@1234567', 
    #         birth_date="1981-09-23",
    #         status=True,
    #     )
    #     # user = CustomUser.objects.get(phone_number=obj.phone_number)
    #     # sample_login = {'phone_number': user.phone_number, 'password': make_password('@1234567')}

    #     # self.authenticate()
    #     # sample_login = {'phone_number': '01067174141', 'password': '@1234567'}
        
    #     response = self.client.post(reverse('custom_login'), header)
        
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    # def test_Model1_detail(self):
    #     users = CustomUser.objects.all()
    #     if users:
    #         response = self.client.get(reverse('Model1-detail', args=[mm_objs[0].id]))
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)


    # def test_get_absolute_url(self):
    #     user = CustomUser.objects.get(id=1)
    #     self.assertEqual(user.get_absolute_url(), "/user/id/1")
