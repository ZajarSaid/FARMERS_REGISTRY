from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.urls import reverse
from User.forms import UserRegister
from django.http import JsonResponse
from User.models import Farmer
from Production.models import District, Region, Crop
from validate_email import validate_email
from django.contrib import messages
from User.models import Farm
from django.views import View
import json


def List_farmers(request):
     all_farmers = Farmer.objects.all()

     return render(request, 'production/_farmers.html', {'farmers':all_farmers})

def List_farms(request):
    all_farms = Farm.objects.all()

    return render(request, 'production/_farms.html', {'farms':all_farms})

def dashboard(request):
    template_name = 'production/dashboard.html'

    farmers = Farmer.objects.all()
    regions = Region.objects.all()
    crops = Crop.objects.all()
    farms = Farm.objects.all()

    context={
        'farmers':farmers,
        'regions':regions,
        'crops':crops,
        'farms':farms
    }
    return render(request, template_name, context)



def home(request):

    template_name = 'production/base.html'

    return render(request, template_name)


def index(request):

    return render(request, 'users/registration.html')

        
def register(request):
    farmers = Farmer.objects.all()
    regions = Region.objects.all()
    crops = Crop.objects.all()

    if request.method == 'POST':
        
        form = UserRegister(request.POST or None, request.FILES)
        if form.is_valid():
            print(form.cleaned_data['email'])
            password=form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.email = form.cleaned_data['email']
            user.save()
            
            print(user.email)
            messages.success(request, 'a user has been created successfuly...')

            return redirect('User:register')
            
    form = UserRegister()
    context = {
        'farmers':farmers,
        'regions':regions,
        'crops':crops, 
        'form':form
    }
    return render(request,'production/register.html', context)

def all_users(request):

    users = Farmer.objects.all()

    return render(request,'users/farmers.html', {'users':users})
    


# def verify_view(request):
#     form = CodeForm(request.POST or None)
#     pk = request.session.get('pk')
#     if pk:
#         user = MyUser.objects.get(pk=pk)
        
#         code = user.code
#         code_user = f"{user.username}: {user.code}"
        
#         if not request.POST:
#             print(code_user)
        
#         if form.is_valid():
#             num = form.cleaned_data.get('number')
            
#             if str(code) == num:
#                 code.save()
#                 login(request, user)
#                 return redirect('register')
#             else:
#                 return redirect('login')
#     return render(request, 'auth/verify.html', {'form':form})


