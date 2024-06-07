from django.urls import path
from . import views


app_name = 'Production'

urlpatterns=[
    path('', views.index, name='index'),
    path('Home/', views.home, name='home'),
    path('Register/', views.register, name='register'),
    path('Dashboard/', views.dashboard, name='dashboard'),
    path('AllFarms/', views.List_farms, name='all-farms'),
    path('AllFarmers/', views.List_farmers, name='all-farmers')
]