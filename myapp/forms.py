from .models import Room
from .models import Profile
from django.forms import ModelForm
from django.contrib.auth.models import User


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['participants','host']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

