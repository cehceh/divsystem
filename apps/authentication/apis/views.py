from rest_framework import serializers, status
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase, TokenVerifyView

from dj_rest_auth.registration.views import RegisterView

from dj_rest_auth.views import LoginView

from django.contrib.auth import authenticate

from .serializers import CustomObtainSerializer, UserTokenSerializer, TokenAPISerializer

from apps.authentication.models import CustomUser


class MyCustomLogin(LoginView):
    '''
        :Managing login process
    '''

    def get_response(self):
        base_response = super(MyCustomLogin, self).get_response()

        #* here you can get specific fields in the login response 
        base_response.data['user'] = {
            'phone_number': self.user.phone_number,
            #* here you can add some fields if you wish to get more in response
        }

        return base_response


class MyCustomRegister(RegisterView):
    '''
        :Managing registration process
    '''
    def create(self, request, *args, **kwargs):    
        base_response = super(MyCustomRegister, self).create(request, *args, **kwargs)
        base_response.data['user'] = {
            'first_name': request.data['first_name'],
            'last_name': request.data['last_name'], 
            'country_code': request.data['country_code'],
            'phone_number': request.data['phone_number'],
            'gender': request.data['gender'],
            'birth_date': request.data['birth_date'],
        }
        
        return base_response


## for task(3)

class TokenObtainPairView(TokenViewBase):
    serializer_class = CustomObtainSerializer

class TokenAPIView(TokenVerifyView):
    serializer_class = TokenAPISerializer





class UserTokenApi(APIView):

    def post(self, request):
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data # Fetch the data form serializer

        # user = authenticate(email=data['email'], password=data['password']) # check for email and password
        user = CustomUser.objects.values('phone_number')
        match = user.filter(id=request.user.id).exists()
        if match:
            obj = user.get(id=request.user.id)
        else:
            obj = [] 
        
        if obj == [] or obj['phone_number'] != data['phone_number']: # check for phone
            raise serializers.ValidationError({'error':'Incorrect phone number'})

        # Generate Token
        refresh = RefreshToken.for_user(obj)

        return Response(
            {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            },
                status=status.HTTP_200_OK
            )



## Another solution for Task(3)
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response

# class CustomAuthToken(ObtainAuthToken):
#     serializers_class = UserTokenSerializer

#     def post(self, request, *args, **kwargs):
#         # serializer = self.serializer_class(
#         #     data=request.data, context={'request': request})
#         serializer = UserTokenSerializer(
#             data=request.data)

#         serializer.is_valid(raise_exception=True)
#         # user = serializer.validated_data['phone_number']
#         user = request.user.id
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'phone_number': user.phone_number
#         }, status=status.HTTP_200_OK)

