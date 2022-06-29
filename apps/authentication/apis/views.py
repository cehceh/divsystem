# from rest_framework.renderers import (
#                                         HTMLFormRenderer, 
#                                         JSONRenderer, 
#                                         BrowsableAPIRenderer,
#                                     )
# from rest_framework import views

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from dj_rest_auth.registration.views import RegisterView

from dj_rest_auth.views import LoginView

# from .serializers import DetailUserSerializer


class MyCustomLogin(LoginView):
    '''
        Managing login process
    '''

    def get_response(self):
        base_response = super(MyCustomLogin, self).get_response()
        # data = {
        #     'phone_number': self.user.phone_number,
        # }
        #* here you can get specific fields in the login response 
        base_response.data['user'] = {
            'phone_number': self.user.phone_number,
            #* here you can add some fields if you wish to get more in response
        }
        # base_response.data.update(data)
        # base_response.data['user']['phone_number'] = self.user.phone_number

        return base_response


class MyCustomRegister(RegisterView):
    '''
        Managing registration process
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


# class DetailUserView(views.APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = DetailUserSerializer
#     renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)

#     def get_queryset(self, *args, **kwargs):
#         user=self.request.user
#         qs = CustomUser.objects.filter(
#             id=user.id
#             ).values(
#                 'id',
#                 'first_name', 
#                 'last_name',
#                 'birth_date',
#                 'country_code',
#                 'phone_number',
#                 'gender'
#             ).first()
        
#         return qs
    
#     def get(self,request, *args, **kwargs):
#         base_response = self.get_queryset()
#         return Response(base_response)
    
#     def post(self,request, *args, **kwargs):
#         initial_data = self.get_queryset()
#         data=request.data
#         user=self.request.user
#         serializer = self.serializer_class(data=data)
#         if serializer.is_valid():
#             # email = data['email'] or initial_data['email'] 
#             phone_number = data['phone_number'] or initial_data['phone_number']
#             username = data['username'] or initial_data['username']
#             first_name = data['first_name'] or initial_data['first_name']
#             last_name = data['last_name'] or initial_data['last_name']
            
#             qs = CustomUser.objects.filter(id=request.user.id)
#             password=qs.first().password[:10]
#             # qs.update(email=email,phone_number=phone_number,username=username)
            
#             base_response = self.get_queryset()
#             return Response(base_response)
#         else:
#             base_response= Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             return base_response

from rest_framework_simplejwt.views import TokenViewBase
from .serializers import CustomObtainSerializer #TokenObtainLifetimeSerializer, TokenRefreshLifetimeSerializer


class TokenObtainPairView(TokenViewBase):

    serializer_class = CustomObtainSerializer


# class TokenObtainPairView(TokenViewBase):
#     """
#         Return JWT tokens (access and refresh) for specific user based on username and password.
#     """
#     serializer_class = TokenObtainLifetimeSerializer


# class TokenRefreshView(TokenViewBase):
#     """
#         Renew tokens (access and refresh) with new expire time based on specific user's access token.
#     """
#     serializer_class = TokenRefreshLifetimeSerializer

