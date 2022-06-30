from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from dj_rest_auth.registration.views import RegisterView

from dj_rest_auth.views import LoginView


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


from rest_framework_simplejwt.views import TokenViewBase
from .serializers import CustomObtainSerializer 


class TokenObtainPairView(TokenViewBase):
    serializer_class = CustomObtainSerializer


