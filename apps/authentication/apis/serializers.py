from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import exceptions, serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from datetime import datetime, date

from django.core.validators import RegexValidator

from django.utils.timezone import utc
from django.contrib.auth import authenticate

from ..models import  CustomUser

import base64
from django.core.files.base import ContentFile


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" or extension == 'png'  else extension

        return extension


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
    # avatar = serializers.ImageField(required=True)
    avatar = Base64ImageField(
        max_length=None, use_url=True, required=True
    )
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
                    ('This phone number is taken .....'),
                )

        # if no user registered with this phone number
        except ObjectDoesNotExist:
            return phone_number


    def validate_birth_date(self, birth_date):
        """
           * :raises: :class:`ValidationError`
           * :birth date must be in format 'YYYY-MM-DD'
           * :and must be in the past
        """
        today = date.today()

        #* check if the birth date is in the future raise an error 
        if birth_date > today: 
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


class CustomLoginSerializer(LoginSerializer):
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



## For task(3) 

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer

from rest_framework_simplejwt.tokens import RefreshToken

class CustomObtainSerializer(TokenObtainPairSerializer):
    """
    *  :Here the solution of "task no.(3)", but for some reasons I can't get rid of 
    *  :The username and password fields, I don't know but 
    *  :I think overriding this class(TokenObtainPairSerializer) is perform the job
    *  :It may need some time to find what's going on, Really I don't know till now
    *  :But with some investigation, It will be fixed. 
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        self.fields["phone_number"] = serializers.CharField()
        self.fields["phone_number"].required = True
        self.fields["access_token"] = serializers.CharField()
        self.fields["access_token"].required = True
        self.fields["status"] = serializers.CharField()
        self.fields["status"].required = True

    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def validate(self, attrs):
        data = super().validate(attrs)

        data['username'] = self.user.username
        data['phone_number'] = self.user.phone_number
        # data['status'] = self.user.status

        authenticate_kwargs = {
            # self.username_field: attrs[self.username_field],
            "phone_number": attrs["phone_number"],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)
        # if self.user:
        #     return data
        # else:
        #     raise exceptions.AuthenticationFailed(
        #         self.error_messages["no_active_account"],
        #         "Something Went Wrong ...",
        #     )

        return data

## Here is the solution of the Task(3)
class TokenAPISerializer(TokenVerifySerializer):
    phone_number = serializers.CharField(required=True)
    status = serializers.CharField(required=True)

    def validate(self, attrs):
        # data = super().validate(attrs)
        token = str(attrs['token'])      #UntypedToken(attrs["token"])
        phone = str(attrs['phone_number'])
        # status = str(attrs['status'])
        
        # from rest_framework.authtoken.models import Token
        # user_obj = CustomUser.objects.get(phone_number=phone)
        # user_token = Token.objects.get_or_create(user_id=user_obj.id)

        # match = Token.objects.filter(user_id=user_obj.id).exists()
        # if match:
        #     token_obj = Token.objects.get(user_id=user_obj.id)
        # else:
        #     token_obj = []

        # print('Token: ', user_token[1],)
        # if user_token[1]:
        return {
            'token': str(token),
            'phone_number': str(phone),
            # 'status': str(status),
        }
        # else:
        #     raise serializers.ValidationError('Credential does not match')
        
        


## Another solution for task(3)

class UserTokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    status = serializers.CharField(required=True)


