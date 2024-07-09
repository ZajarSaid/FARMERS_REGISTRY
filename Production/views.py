from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponsePermanentRedirect, HttpResponse

from django.core.mail import send_mail
from django.conf import settings

from django.urls import reverse
from User.forms import UserRegister
from django.views import View
from django.http import JsonResponse
from User.models import Farmer
from io import BytesIO  # Import BytesIO

from Production.models import District, Region, Crop
from django.contrib import messages
from User.models import Farm, OutputVerification, Farm
from .forms import MarketPriceForm, UpdateFarmForm
from .models import RegionalPrices
from django.db.models import Sum
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import pandas as pd
from .utils import OutputVerificationUtil

from .serializer import FarmSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView



def RegionalPriceTrends(LoginRequiredMixin,  View):
    template_name = 'production/PriceTrends.html'




class FarmOutputTrendsView(TemplateView):
    template_name = 'production/General_analysis.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = Region.objects.all()
        context['farms'] = Farm.objects.all()
        total = 0
        
        context['output'] = Farm.objects.aggregate(total_output=Sum('total_output'))
        return context
    
        

class FarmDataAPIView(APIView):
    def get(self, request):
        farms = Farm.objects.all()
        region_id = request.GET.get('region')
        if region_id:
            farms = farms.filter(region_id=region_id)

        crop_output = farms.values('crop_type__name', 'region__name').annotate(total_output=Sum('total_output')).order_by('crop_type')
        data = [{'crop_name': item['crop_type__name'], 'total_output': item['total_output']} for item in crop_output]

        total_farms = farms.count()
        total_output = farms.aggregate(Sum('total_output'))['total_output__sum']

          # Print data for debugging
        print("Filtered Farms:", farms)
        print("Crop Output:", crop_output)

        return Response(data)


class ModifyRegionalPricesView(LoginRequiredMixin, View):
    template_name = 'Production/_modifyregionalprice.html'

    def get(self, request, rp_id):
        # take the id of specified regional_price
        
        rp = get_object_or_404(RegionalPrices, pk=rp_id)

        form = MarketPriceForm(instance=rp)
        context={
            'form':form
        }

        def post(self, request, rp_id):
            rp = get_object_or_404(RegionalPrices, pk=rp_id)

            form = MarketPriceForm(instance=rp)
            if form.is_valid():
                form.save()
                messages.success(request, 'regional price updated successfuly.')
                return redirect('Production:modify-regional-prices')


        return render(request, self.template_name, context)

@login_required
def add_regional_prices(request):
    template_name = 'production/add_regional-prices.html'

    if request.method == 'POST':
        form = MarketPriceForm(request.POST or None)

        if form.is_valid():
            region = request.POST.get('region')
            crop = request.POST.get('crop')

            # check the existing same values in the table for that form instance
            existing_instance = RegionalPrices.objects.filter(region=region, crop=crop)
            if not existing_instance:
                form.save()
                messages.success(request, 'the price has been added succesfuly..')
                return redirect('Production:regional-prices')
                
            else:

                # region_name = [e.region.name for e in existing_instance]
                # crop_name = [e.crop.name for e in existing_instance]

                # c_name = crop_name[0]
                # r_name = region_name[0]
                # r_name = str.upper(r_name)

                # OR

               for e in existing_instance:
                c_name = e.crop
                r_name = e.region
            
                # r_name = str.upper(r_name)
                print(type(r_name))
                print(type(Farmer))

                messages.error(request, f'There is already regional price of {c_name} in  {r_name}')
                return redirect('Production:regional-prices')

        else:
            pass

    form = MarketPriceForm()

    context={
        'form':form
    }

    return render(request, template_name, context)


# this view has no template
class RegionalAnalysisView(LoginRequiredMixin, View):
    def get(self, request):
        farms = Farm.objects.all()
        data = {
            'Region': [farm.region.name for farm in farms],
            'Total Output': [farm.total_output for farm in farms],
            'Month': [farm.c_s_date.strftime('%Y-%m') for farm in farms]
        }
        df = pd.DataFrame(data)
        regional_output = df.groupby('Region')['Total Output'].sum().reset_index()

        plt.figure(figsize=(10, 6))
        sns.barplot(x='Region', y='Total Output', data=regional_output)
        plt.title('Total Output by Region')
        plt.xlabel('Region')
        plt.ylabel('Total Output')
        plt.xticks(rotation=45)

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        regional_output_plot = base64.b64encode(image_png).decode('utf-8')

        context = {
            'regional_output': regional_output.to_dict('records'),
         
            'regional_output_plot': regional_output_plot,
        }

        return render(request, 'production/regional_production_analysis.html', context)



class NationalAnalysisView(View):
    template_name = 'production/nationalAnalysis.html'

    def get(self, request):
        # Fetch all farms
        farms = Farm.objects.all()

        # Create a DataFrame
        data = {
            'Region': [farm.region.name for farm in farms],
            'Total Output': [farm.total_output for farm in farms],
            'Month': [farm.c_s_date.strftime('%Y-%m') for farm in farms]
        }
        df = pd.DataFrame(data)

        # National Total Output
        national_output = df['Total Output'].sum()

        # Monthly Total Output Evolution
        monthly_output = df.groupby('Month')['Total Output'].sum().reset_index()

        # Plotting
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Month', y='Total Output', data=monthly_output)
        plt.title('Monthly Total Output Evolution')
        plt.xlabel('Month')
        plt.ylabel('Total Output')
        plt.xticks(rotation=45)

        # Save plot to a bytes buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        #Encode plot to base64 string
        monthly_output_plot = base64.b64encode(image_png).decode('utf-8')

        context = {
            'national_output': national_output,
            'monthly_output': monthly_output.to_dict('records'),
            'monthly_output_plot': monthly_output_plot,
        }

        return render(request, self.template_name, context)

class CropsView(LoginRequiredMixin, View):
    template_name = 'production/all_crops.html'

    def get(self, request):

        crops = Crop.objects.all()

        context = {
            'crops':crops
        }

        return render(request, self.template_name, context)

class RegionalPriceView(LoginRequiredMixin, View):
    template_name = 'production/_RegionalPrices.html'

    def get(self, request):
        all_r_prices = RegionalPrices.objects.all()

        context = {
            
            'market_prices':all_r_prices
        }

        return render(request, self.template_name, context)

        

class FarmerDetailsView(LoginRequiredMixin, View):
    template_name = 'production/_FarmerDetails.html'

    def get(self, request, f_username):
        form = UpdateFarmForm()
        s_farmer = get_object_or_404(Farmer, username=f_username)

        # check if there are output verification instances of similar farm
        all_verifications = OutputVerification.objects.filter(owner=s_farmer)
        
        if all_verifications:
            print(all_verifications)
        

        context = {
            'farmer':s_farmer,
            'form' : form
        }

        return render(request, self.template_name, context)

    def post(self, request, f_username):
        farmer_id = request.POST['farmer_id']
        farm_name = request.POST['farm_name']
        output = request.POST['farm_output']

        

        try:
            farm_output = get_object_or_404(Farm, name=farm_name, owner=farmer_id)
            farm_output.total_output = output
            farm_output.save()  


            subject = 'New output is placed'
            message = 'dear farmer '
            # email = 'zajarjafary@gmail.com'
            # recipient_list = [email]

            send_mail(subject, message, settings.EMAIL_HOST_USER, ['zajarjafary@gmail.com'], fail_silently=True)
            print(send_mail)
            
        # logic to save verification_output_farm........
        # Get the farmer instance
            farmer = get_object_or_404(Farmer, id=farmer_id)

        #    check if there is previous instance by looking its name
            previous_verification_instance = OutputVerification.objects.filter(owner=farmer)
            if previous_verification_instance:
                previous_verification_instance.delete()
            print(previous_verification_instance)
         # Create the output verification instance
            OutputVerificationUtil.create_output_verification(
                owner=farmer,
                farm_name=farm_name,
                farm_output=output
            )

            messages.success(request, 'Farm profile has been updated successfully.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

        return redirect('Production:farmer-details', f_username=f_username)



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

    return render(request, 'production/base.html')

        
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
    




