from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.urls import reverse

from django.http import JsonResponse
from .models import Farmer, Farm, Rank, OutputVerification
from Production.models import District, Region, Crop, RegionalPrices
from .forms import UserRegister
from validate_email import validate_email
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views import View
import json
from django.views.generic import TemplateView




class ChangePasswordView(LoginRequiredMixin, View):
    template_name = 'users/Change_password.html'

    def get(self, request):

        return render(request, self.template_name)

    def post(self, request):
        # take form data
        current_password = request.POST['currentPassword']
        new_password = request.POST['newPassword']
        confirm_password = request.POST['confirmPassword']
        f_pk = request.user.pk

        # take current user password then confirm the algorithm
        farmer = get_object_or_404(Farmer, pk=f_pk)
        if farmer:
            print(c_password)
            if current_password == farmer.password:
                if new_password == confirm_password:
                    newfarmer = farmer.save(commit=False)
                    newFarmer.password = newFarmer.set_password(confirm_password)
                    newFarmer.save()
                    messages.success(request, 'your password has been changed successfuly..!')
                    return redirect('User:change-password')
                else:
                    messages.error(request, "two passwords didn't match")
            else:
                messages.error(request, 'wrong password')
                return redirect('User:change-password')

        return render(request, self.template_name)



def verify_ouput(request, f_id):
    # take output_verification related to farmer_id
    # if present, assign a verified value then return a message to verify the process
    status = 'verified'
    output_instance = get_object_or_404(OutputVerification, owner=f_id)
    output_instance.status = status
    farmer = Farmer.objects.filter(pk=f_id)
    print(farmer)
    output_instance.save()

    # OutputVerification.objects.update_or_create(
    #             status=status,
    #             defaults={'owner': farmer},
    #         )
    messages.success(request, 'Your farm has been registered and ranked in the database of farmers effectively ')

    return redirect('User:home-page')
 


class RegionalPriceView(LoginRequiredMixin, TemplateView):
    template_name = 'users/regional_prices.html'

    def get(self, request):
        farmer = request.user
        farms = Farm.objects.filter(owner=farmer)
        crops = farms.values_list('crop_type', flat=True).distinct()
        regional_prices = RegionalPrices.objects.filter(crop_id__in=crops)

        context = {
            'regional_prices': regional_prices,
        }
        return render(request, self.template_name, context)


@login_required
def regional_prices_view(request):
    farmer = request.user
    farms = Farm.objects.filter(owner=farmer)
    crops = farms.values_list('crop_type', flat=True).distinct()
    regional_prices = RegionalPrices.objects.filter(crop_id__in=crops)

    context = {
        'regional_prices': regional_prices,
    }
    return render(request, 'regional_prices.html', context)



class FarmerHistoryView(LoginRequiredMixin, View):
    template_name = 'users/farmer_dashboard.html'

    def get(self, request):
        farmer = request.user
        farms = Farm.objects.filter(owner=farmer)
        try:
            rank = Rank.objects.get(farmer=farmer)
        except Rank.DoesNotExist:
            rank = None

        context = {
            'farmer': farmer,
            'farms': farms,
            'rank': rank,
        }
        return render(request, self.template_name, context)


@login_required
def farmer_dashboard(request):
    farmer = request.user
    farms = Farm.objects.filter(owner=farmer)
    try:
        rank = Rank.objects.get(farmer=farmer)
    except Rank.DoesNotExist:
        rank = None

    context = {
        'farmer': farmer,
        'farms': farms,
        'rank': rank,
    }
    return render(request, 'users/farmer_dashboard.html', context)


@login_required
def farmer_index(request):
    farmer = request.user
    farms = Farm.objects.filter(owner=farmer)
    # user_verification = get_object_or_404(OutputVerification, owner=farmer)
    # if user_verification:
        
    #     print(user_verification)
    try:
        user_verification = OutputVerification.objects.filter(owner=farmer)
        if user_verification:
            print(user_verification)

        else:

        
            print('there is no output verification for you...')

    except user_verification.DoesNotExist:
        user_verification = None

    output = 0
    crops = []
    Number_Crops = 0

    if farms:
        for item in farms:
            crops.append(item.crop_type)
            Number_Crops += 1
            output += item.total_output

    try:
        rank = Rank.objects.get(farmer=farmer)
    except Rank.DoesNotExist:
        rank = None

    context = {
        'farmer': farmer,
        'farms': farms,
        'rank': rank,
        'output':output,
        'crops':Number_Crops,
        'output_verification':user_verification
    }

    return render(request, 'users/farmer_index.html', context)



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
        image = request.FILES.get('image')

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
                 address=address,
                 image=image
                 )
                user.set_password(password)
                user.save()
                messages.success(request, 'A farmer account has been created successfuly..')
                return redirect('User:user-register')

                return render(request, 'users/registration.html')

        return render(request, self.template_name)

#Farm Registration View
class RegisterFarmView(LoginRequiredMixin, View):
    template_name = 'users/registerFarm.html'
    login_url = 'User/UserLogin/'  # URL to redirect to if the user is not logged in

    def get(self, request):
        regions = Region.objects.all()
        districts = District.objects.all()
        crop_types = Crop.objects.all()
        Farmers = Farmer.objects.all()

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
        owner = get_object_or_404(Farmer, id=request.user.id)

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
        return redirect('User:farmer-account')  


class FarmerAccountView(View):
    template_name = 'users/FarmerPage.html'

    def get(self, request):

        user_pk = request.user.pk
        FarmerInfo = get_object_or_404(Farmer, pk=user_pk)

        if FarmerInfo.is_superuser:
            return redirect('Production:dashboard')

        form = UserRegister(instance=FarmerInfo)
        user = FarmerInfo
        context = {
            'form':form,
            'user':user
            }    


        return render(request, self.template_name, context)

    def post(self, request):

        user_pk = request.user.pk
        real_farmer = get_object_or_404(Farmer, pk=user_pk)
        form = UserRegister(request.POST, request.FILES, instance=real_farmer)
        print(form)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your information has been updated successfuly..')
            return redirect('User:farmer-account')

        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        # email = request.POST['email']
        # username = request.POST['username']
        # image = request.FILES.get('image')
        # phone = request.POST['phone']

        # farmer = Farmer.objects.get(id=user_pk)

        # farmer.username = username
        # farmer.last_name = last_name
        # farmer.first_name = first_name
        # farmer.email = email
        # farmer.image = image
        # farmer.phone = phone
        # farmer.save()
        messages.error(request, 'Your information has not been updated successfuly..')

        return redirect('User:farmer-account')


    def post(self, request):

        return render(request, self.template_name)

def index(request):
    # the index should return index page as a website initial page where,
    # users can  navigate different sections about the system like login and registration
    # currently it returns a farmer registration page for development/testing purposes

    return render(request, 'users/Home.html')

    

def user_login(request):
    
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        #return back the email if only passwords are not matched
   
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['pk'] = user.pk

            login(request,user)
            messages.success(request, 'You have been logged in successfuly')
            
            if user.is_superuser:
                return redirect('Production:dashboard')
            return redirect('User:home-page')
        messages.error(request, " There's an error logging in")
        
    return render(request, 'users/login.html')



def user_logout(request):
    logout(request)
    return HttpResponsePermanentRedirect(reverse('User:index'))

