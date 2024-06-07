from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.urls import reverse

from django.http import JsonResponse
from .models import Farmer
from Production.models import District, Region, Crop
from validate_email import validate_email
from django.contrib import messages
from User.models import Farm
from django.utils import timezone
from django.views import View
import json


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric character'})
        if Farmer.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'username is already taken, choose another'})
        return JsonResponse({'username_valid':True})
    
    
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'email is invalid'}, status=400)
        if Farmer.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'this email is already taken, choose another'})
        return JsonResponse({'email_valid':True})


class LoadDistrictsView(View):
    # we load districts from the database related to selected region as a query parameter (region_id) 
    # return them as a list
    def get(self, request):
        region_id = request.GET.get('region_id')
        if region_id:
            districts = District.objects.filter(region__id=region_id).values('id', 'name')
            return JsonResponse(list(districts), safe=False)
        return JsonResponse({'error': 'Invalid region ID'}, status=400)

# Farmer Registration view
class FarmerRegistrationView(View):
    template_name = 'users/registration.html'

    def get(self, request):

        return render(request, self.template_name)

    def post(self, request):
        #GET USER DATA
        #VALIDATE
        #Create a user Account

        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']

        context = {'FieldValues':request.POST}

        if not Farmer.objects.filter(username=username).exists():
            if not Farmer.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'your password is too short')

                    return render(request, 'users/registration.html', context)

                # the default value of status is MediumFarmer
                user = Farmer.objects.create_user(
                 username=username,
                 first_name=firstname,
                 last_name=lastname,
                 email=email,
                 phone=phone,
                 address=address
                 )
                user.set_password(password)
                user.save()
                messages.success(request, 'A user account has been created successfuly..')
                return redirect('User:user-register')

                return render(request, 'users/registration.html')

        return render(request, self.template_name)

#Farm Registration View
class RegisterFarmView(View):
    template_name = 'users/registerFarm.html'

    def get(self, request):
        regions = Region.objects.all()
        districts = District.objects.all()
        crop_types = Crop.objects.all()
        context = {
            'regions': regions,
            'crop_types': crop_types,
            'districts': []
        }
        return render(request, self.template_name, context)

    def post(self, request):
        name = request.POST.get('farmname')
        size = request.POST.get('size')
        crop_type_id = request.POST.get('crop_type')
        region_id = request.POST.get('region')
        district_id = request.POST.get('district')
        owner = request.user  

        print(region_id)
        print(district_id)
        print(request.POST)

        if not name:
            messages.error(request, 'A farm must have a name.')
        if not size:
            messages.error(request, 'A farm must have a size.')
        if not crop_type_id:
            messages.error(request, 'A crop type is required.')
        if not region_id:
            messages.error(request, 'A region is required.')
        if not district_id:
            messages.error(request, 'A district is required.')

        if not name or not size or not crop_type_id or not region_id or not district_id:
            
            regions = Region.objects.all()
            districts = District.objects.all()
            crop_types = Crop.objects.all()
            context = {
                'regions': regions,
                'districts': districts,
                'crop_types': crop_types
            }
            return render(request, self.template_name, context)
        
        # taking the crop, region and district from the database similar to what a user has just selected 
        
        crop_type = get_object_or_404(Crop, id=crop_type_id)
        region = Region.objects.get(id=region_id)
        district = District.objects.get(id=district_id)

        # Create and save the Farm instance
        farm = Farm.objects.create(
            name=name,
            size=size,
            crop_type=crop_type,
            region=region,
            district=district,
            owner=owner,
            c_s_date=timezone.now(),  
            total_output=0,    #
            
        )
        
        farm.save()

        messages.success(request, 'Farm registered successfully!')
        return redirect('User:login')  


def index(request):
    # the index should return index page as a website initial page where,
    # users can  navigate different sections about the system like login and registration
    # currently it returns a farmer registration page for development/testing purposes

    return render(request, 'users/base.html')

    

def user_login(request):
    
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['pk'] = user.pk
            login(request,user)
            messages.info(request, 'You have been logged in successfuly')
            return redirect('Production:dashboard')
    return render(request, 'users/login.html')


def user_logout(request):
    logout(request)
    return HttpResponsePermanentRedirect(reverse('User:login'))

