# from django.contrib.sites import requests
# from django.core.exceptions import ValidationError
from django.db.models import Q

from allauth.account.adapter import DefaultAccountAdapter

from apps.authentication.models import CustomUser


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.phone_number = data.get('phone_number')
        # user.last_name = data.get('last_name')
        
        user.username = user.phone_number   #data.get('username')
        user.email = data.get('email')
        user.save()  

        return user

