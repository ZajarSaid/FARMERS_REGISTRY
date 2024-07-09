from django.urls import path
from . import views
from .views import LoadDistrictsView, RegisterFarmView, UsernameValidationView, EmailValidationView
from .views import FarmerRegistrationView, FarmerAccountView, FarmerHistoryView, RegionalPriceView, ChangePasswordView
from django.views.decorators.csrf import csrf_exempt

app_name = 'User'

urlpatterns=[
    path('', views.index, name='index'),
    path('UserLogin/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('Index/', views.farmer_index, name='home-page'),
    path('RegisterFarm/', RegisterFarmView.as_view(), name='register-Farm'),
    path('LoadDistricts/', LoadDistrictsView.as_view(), name='load-districts'),
    path('RegisterFarmer/', FarmerRegistrationView.as_view(), name='user-register'),
    path('email-validate/', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('FarmerAccount/', FarmerAccountView.as_view(), name='farmer-account'),
    path('FarmerHistory/', FarmerHistoryView.as_view(), name='farmer-history'),
    path('RegionalPrices/', RegionalPriceView.as_view(), name='regional-prices'),
    path('Verify-output/<int:f_id>', views.verify_ouput, name='verify-output'),
    path('ChangePassword/', views.ChangePasswordView.as_view(), name='change-password')
    


]