from django.urls import path
from dj_rest_auth.views import LogoutView
from .apis.views import TokenObtainPairView #, TokenRefreshView

from django.conf import settings

from .apis.views import (
    # DetailUserView,
    MyCustomRegister,
    MyCustomLogin,
)



urlpatterns = [    

    # path("user/", DetailUserView.as_view(), name="edit_user"),
    
    path('register/', MyCustomRegister.as_view(), name='custom_register'),
    path('login/', MyCustomLogin.as_view(), name='custom_login'),
    path('logout/', LogoutView.as_view()),
    
    path('token/obtain/', TokenObtainPairView.as_view(), name='token_obtain'),

]

if getattr(settings, 'REST_USE_JWT', False):
    from rest_framework_simplejwt.views import TokenVerifyView

    from dj_rest_auth.jwt_auth import get_refresh_view

    urlpatterns += [
        path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
        path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),

    ]



