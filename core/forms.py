'''
Created on Jun 5, 2012

@author: chrisduranti
'''
from django import forms
from django.forms import ValidationError
from django.forms.widgets import RadioSelect
from django.db import transaction
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login
from models import Person, Activation, PasswordReset
import uuid
from util import send_reset
from django.contrib.auth.hashers import make_password

class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs = {'placeholder' : 'Username'}), required = False)
    password = forms.CharField(widget=forms.PasswordInput(attrs = {'placeholder' : 'Password'}), required = False)

        
    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self.request = args[0]
            super(LoginForm, self).__init__(args[0].POST)
        else:
            super(LoginForm, self).__init__(*args, **kwargs)

    def save(self):
        self.success = True

    def clean_username(self):
        val = self.cleaned_data['username']
        if len(val) < 1:
            raise ValidationError('Please enter a username')
        return val

    def clean_password(self):
        val = self.cleaned_data['password']
        if len(val) < 1:
            raise ValidationError('Please enter a password')
        return val

    def clean(self):
        if not self.errors:
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    login(self.request, user)
                else:
                    raise ValidationError('Your account is not active')
            else:
                raise ValidationError('Your login credentials were invalid')


class ResetForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput(attrs = {'placeholder' : 'Password'}), required = False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs = {'placeholder' : 'Confirm Password'}), required = False)


    def save(self, key):
        self.success = True
        reset = PasswordReset.objects.get(key = key)
        user = reset.user
        user.password = make_password(self.cleaned_data['password'])
        user.save()
        reset.delete()



    def clean_password(self):
        val = self.cleaned_data.get('password', '')
        if len(val) < 1:
            raise ValidationError('Please enter a password')
        return val

    def clean_password2(self):
        val = self.cleaned_data.get('password2', '')
        if len(val) < 1:
            raise ValidationError('Please enter the second password')
        return val


    def clean(self):
        if not self.errors:
            p1 = self.cleaned_data['password']
            p2 = self.cleaned_data['password2']
            if p1 != p2:
                raise ValidationError('Your passwords do not match')
            return self.cleaned_data

class RetrieveForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs = {'placeholder' : 'Username'}), required = False)

    def save(self):
        self.success = True
        reset = PasswordReset(key = str(uuid.uuid4()), user = self.user)
        reset.save()
        send_reset(self.user, reset)



    def clean_username(self):
        val = self.cleaned_data['username']
        if len(val) < 1:
            raise ValidationError('Please enter a username')
        try:
            self.user = User.objects.get(username = val)
        except User.DoesNotExist:
            raise ValidationError('That user does not exist')
        return val


    
    
class RegisterForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs = {'placeholder' : 'Username'}), required = False)
    password = forms.CharField(widget=forms.PasswordInput(attrs = {'placeholder' : 'Password'}), required = False)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs = {'placeholder' : 'Confirm Password'}), required = False)
    email = forms.EmailField(widget=forms.TextInput(attrs = {'placeholder' : 'Email'}))
        
    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']
        user = User.objects.create_user(username = username, email = email, password = password)
        user.save()
        person = Person(user = user, verified = True, email = email, name = username)
        person.save()
        self.person = person
        activate = Activation(key = str(uuid.uuid4()), person = person)
        activate.save()
        self.activate = activate
        self.success = True
        return (self.person, self.activate)
    

    def clean_username(self):
        val = self.cleaned_data['username']
        if len(val) < 1:
            raise ValidationError('Please enter a username')
        if User.objects.filter(username = val).exists():
            raise ValidationError('Someone already has that username')
        return val

    def clean_password(self):
        val = self.cleaned_data['password']
        if len(val) < 1:
            raise ValidationError('Please enter a password')
        return val

    def clean(self):
        if not self.errors:
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            password2 = self.cleaned_data['password2']
            email = self.cleaned_data['email']
            if password != password2:
                raise ValidationError('Your passwords don\'t match')
            return self.cleaned_data
            