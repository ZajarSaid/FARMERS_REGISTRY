from django.urls import path
from . import views
from .views import LoadDistrictsView, RegisterFarmView, UsernameValidationView, EmailValidationView, FarmerRegistrationView
from django.views.decorators.csrf import csrf_exempt

app_name = 'User'

urlpatterns=[
    path('', views.index, name='index'),
    path('UserLogin/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('RegisterFarm/', RegisterFarmView.as_view(), name='register-Farm'),
    path('LoadDistricts/', LoadDistrictsView.as_view(), name='load-districts'),
    path('RegisterFarmer/', FarmerRegistrationView.as_view(), name='user-register'),
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name='validate-username')

]