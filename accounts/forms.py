from django.contrib.auth.forms import UserCreationForm
from .models import Account
from django import forms


class RegistrationForm(UserCreationForm):
    
    email = forms.EmailField(required=True)
    phone_number = forms.IntegerField(required=False) 
    def save(self,commit=True,*args, **kwargs):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # hash the password
        user.is_active = True  # optional: activate on creation
        user.is_superuser=False
        if commit:
            user.save()
        return user
    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2']
