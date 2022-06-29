from xmlrpc.client import DateTime
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from datetime import datetime, date

from django.core.validators import RegexValidator

from django.utils.timezone import utc

from ..models import  CustomUser


class CustomRegisterSerializer(RegisterSerializer):
    username = None #serializers.CharField(max_length=20, required=False, write_only=True)
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)

    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{11,15}$")
    phone_number = serializers.CharField(
        validators =[phoneNumberRegex], 
        max_length=16, required=True
    )
    
    country_code = serializers.CharField(max_length=20, required=True)
    CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = serializers.ChoiceField(choices=CHOICES)
    avatar = serializers.ImageField(required=True)
    # birth_date = serializers.CharField(required=True)
    birth_date = serializers.DateField(format="%Y-%m-%d", input_formats=['%Y-%m-%d',], required=True)
    
    #* how do you need email field 'required=False'(it is not BOLD) and you want a validation of (error: taken)
    #* the empty field will repeat many times and raise a validation error
    email = serializers.EmailField(max_length=30, required=False) 
    
    
    def validate_email(self, email):
        '''
            :param email: The registered user email
            :type email: email
            
            :return: email 
            
            :raises: :class:`ValidationError`: if email already exist in the db

            check if email exist or not
        '''
        try:
            #* here we use .values() for enhance performance instead of .get() directly
            user = CustomUser.objects.values('email') 
            user_email = user.get(email=email)
            if user_email['email']:
                raise serializers.ValidationError(
                    'This email is already exists .... '
                )
        except ObjectDoesNotExist:
            return email


    def validate_phone_number(self, phone_number):
        """
            :param phone_number: The registered user phone number
            :type phone_number: str
            
            :return: phone_number 
            
            :raises: :class:`ValidationError`: if mobile already exist in the db

            check if mobile exist or not
        """

        try:
            user = CustomUser.objects.values('phone_number')
            phone = user.get(phone_number=phone_number)
            if phone['phone_number']:
                raise serializers.ValidationError(
                    ('This user is already registered with this phone number .'),
                )

        # if no user registered with this phone number
        except ObjectDoesNotExist:
            return phone_number


    def validate_birth_date(self, birth_date):
        """
           * :raises: :class:`ValidationError`: 
           * :birth date must be in format 'YYYY-MM-DD'
           * and must be in the past
        """
        today = date.today()

        date_compare = (today.month, today.day) < ((birth_date).month, (birth_date).day)
        dt = today.year - (birth_date).year - date_compare

        #* check if the birth date is in the future raise an error 
        if dt == -1: 
            raise serializers.ValidationError('Birth date must be in the past') 

        return birth_date


    
    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['id'] = self.validated_data.get('id', '')
        data_dict['first_name'] = self.validated_data.get('first_name', '')
        data_dict['last_name'] = self.validated_data.get('last_name', '')
        data_dict['country_code'] = self.validated_data.get('country_code', '')
        data_dict['gender'] = self.validated_data.get('gender', '')
        data_dict['phone_number'] = self.validated_data.get('phone_number', '')
        data_dict['birth_date'] = self.validated_data.get('birth_date', '')

        return data_dict

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        """
            :param request: 
            
            :return: user 
            make sure to assign user phone number to his account 
        """
        user = super().save(request)
        
        user.phone_number = self.data.get('phone_number')

        user.save()
        
        return user




class CustomLOGINSERIALIZER(LoginSerializer):
    username = serializers.CharField(label='Phone Number',required=True)
    email = None

    def authenticate(self, **kwargs):
        """
            :param kwargs: 
            :type kwargs: dict
            
            :return: user 
            :type: User object
        """
        try:
            user = CustomUser.objects.get(phone_number=kwargs['username'])
            if user.check_password(kwargs['password']):
                return user
        except ObjectDoesNotExist:
            return None




# class DetailUserSerializer(serializers.ModelSerializer):
#     phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{11,15}$")
#     phone_number = serializers.CharField(
#         validators =[phoneNumberRegex], 
#         max_length=16, required=True
#     )

#     status = serializers.BooleanField(read_only=True, default=False)
#     class Meta:
#         model = CustomUser
#         fields = [
#             "phone_number",
#             "status",
#         ]

            
#     def validate_phone_number(self, phone_number):
#         """
#         """

#         try:
#             user = CustomUser.objects.values('phone_number')
#             match = user.filter(phone_number=phone_number).exists()
#             if not match:
#                 raise serializers.ValidationError(
#                     ('You must registered with this phone number first ....'),
#                 )
#         # if no user registered with this phone number
#         except ObjectDoesNotExist:
#             return phone_number




from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from rest_framework_simplejwt.tokens import RefreshToken

class CustomObtainSerializer(TokenObtainPairSerializer):
    # username = serializers.CharField(label='Phone Number',required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["phone_number"] = serializers.CharField()
        self.fields["phone_number"].required = True
        self.fields["access"] = serializers.CharField()
        self.fields["access"].required = True
        self.fields["status"] = serializers.CharField()
        self.fields["status"].required = True



    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['phone_number'] = user.phone_number
        token['status'] = user.status
        # ...
        print('TOKEN: ', token, 'ACCESS', token['phone_number'])
        return token
    
    # def validate(self, attrs):
    #     data = super().validate(attrs)
    #     refresh = self.get_token(self.user)
        
    #     # data['phone_number'] = self.user.phone_number
    #     # data['status'] = self.user.status
    #     # data['access'] = str(refresh.access_token)
    #     attrs.update({
    #         # 'password': '',
    #         'phone_number': self.user.phone_number,
    #         'status': self.user.status,
    #         'access': str(refresh.access_token),
    #     })

    #     return data

# class TokenObtainLifetimeSerializer(TokenObtainPairSerializer):

#     def validate(self, attrs):
#         data = super().validate(attrs)
#         refresh = self.get_token(self.user)
#         data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())
#         return data


# class TokenRefreshLifetimeSerializer(TokenRefreshSerializer):

#     def validate(self, attrs):
#         data = super().validate(attrs)
#         refresh = RefreshToken(attrs['refresh'])
#         data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())
#         return data
