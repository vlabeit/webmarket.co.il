from django import forms
#from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.forms import fields
from django.forms.widgets import ClearableFileInput
from .models import Profile, CustomUser #PhoneModel

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from captcha.widgets import ReCaptchaV2Invisible

class MyClearableFileInput(ClearableFileInput):
    initial_text = ''
    input_text = ''

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    #age = forms.CharField()
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']


class AuthenticationFormNew(AuthenticationForm):
    required_checkbox = forms.BooleanField(required=False)
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
    


class LoginForm(LoginView):
    email = forms.EmailField()
    #age = forms.CharField()
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_numbers']
        


from django.core.files.storage import default_storage as storage


        

class ProfileUpdateForm(forms.ModelForm):

    image = forms.ImageField(label=('Company Logo'),required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ['image', 'city', 'apart', 'street', 'dob', 'zipcode',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['image'].widget.attrs.update(
            {'class': 'form-control', 'type': 'file', 'id': 'formFile'})
 
  