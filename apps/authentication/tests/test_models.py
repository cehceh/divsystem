from django.test import TestCase
from ..models import CustomUser
# Create your tests here.


class CustomUserTestcase(TestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     obj = CustomUser.objects.create(
    #         username='root',
    #         email="amr.jobmail@gmail.com",
    #         first_name="Amr", 
    #         last_name="Amer", 
    #         country_code="EG",
    #         gender="male",
    #         phone_number="01067174141",
    #         birth_date="1981-09-23",
    #         status=True,
    #     )

    def test_string_method(self):
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
        user = CustomUser.objects.get(id=obj.id)
        expected_string = f"{user.phone_number}"
        self.assertEqual(str(user.phone_number), expected_string)

