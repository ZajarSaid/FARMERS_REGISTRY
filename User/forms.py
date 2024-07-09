from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Farmer, Farm
from django import forms


class UserRegister(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ('username','first_name','last_name', 'email', 'phone', 'address', 'password','image')

        # ('username', 'status')
        
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control', 'placeholder':'username'}),
            'first_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'first_name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'last_name'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email'}),
            'phone':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Contact'}),
            'address':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter address'}),
            'password':forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password'}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
        }

class LoginForm(AuthenticationForm):
    class Meta:
        model = Farmer
        fields = ('email', 'password')


        widgets={
            'email':forms.EmailInput(attrs={
                'class':'form-control'
            }),
            'password':forms.PasswordInput(attrs={'class':'form-control'})
        }
       
class FarmRegister(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ('name','size','crop_type', 'region', 'district','total_output')
        
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'name'}),
            'size':forms.TextInput(attrs={'class':'form-control', 'placeholder':'first_name'}),
            'crop_type':forms.Select(attrs={'class':'form-control', 'placeholder':'last_name'}),
            'region':forms.Select(attrs={'class':'form-control', 'placeholder':'Enter Email'}),
            'district':forms.Select(attrs={'class':'form-control', 'placeholder':'Enter Contact'}),
            
            
        }
    