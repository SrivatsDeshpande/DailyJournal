from .models import User, Entry
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['record','highlight','mood']