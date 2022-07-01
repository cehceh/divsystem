from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.authentication.models import CustomUser


class SignInViewTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
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
            status="True",
        )
        self.user.save()
        self.url = reverse('custom_login')

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        response = self.client.post(self.url, {'username': '01067174141', 'password': '@1234567'})
        # print('DATA: ', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print('DATA::: ', response.data)

    def test_wrong_username(self):
        response = self.client.post(reverse('custom_login'), {'username': 'amr', 'password': '@1234567'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # print('DATA_1: ', response.data)
        # self.assertFalse(response.data['authenticated'])

    def test_wrong_password(self):
        response = self.client.post(reverse('custom_login'), {'username': 'root','password': 'wrong'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # print('DATA_2: ', response.data)