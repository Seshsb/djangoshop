from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class SearchForm(forms.Form):
    search_product = forms.CharField(max_length=880)


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


