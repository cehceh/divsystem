from django.urls import path
from dj_rest_auth.views import LogoutView

from django.conf import settings

from .apis.views import (
    # DetailUserView,
    MyCustomRegister,
    MyCustomLogin,
)



urlpatterns = [    

    # path("user/", DetailUserView.as_view(), name="edit_user"),
    
    path('register/', MyCustomRegister.as_view(), name='custom_rest_register'),
    path('login/', MyCustomLogin.as_view(), name='custom_rest_login'),
    path('logout/', LogoutView.as_view()),

]

if getattr(settings, 'REST_USE_JWT', False):
    from rest_framework_simplejwt.views import TokenVerifyView

    from dj_rest_auth.jwt_auth import get_refresh_view
    from .apis.views import TokenObtainPairView #, TokenRefreshView

    urlpatterns += [
        path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
        path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),

        path('token/obtain/', TokenObtainPairView.as_view(), name='token-obtain'),
        # path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    ]



