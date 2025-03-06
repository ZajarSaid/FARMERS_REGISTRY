from django.urls import path
from . import views
from .views import FarmerDetailsView, RegionalPriceView, CropsView , FarmOutputTrendsView
from .views import NationalAnalysisView, ModifyRegionalPricesView, FarmDataAPIView, UserProfileView


app_name = 'Production'

urlpatterns=[
    path('', views.index, name='index'),
    path('Home/', views.home, name='home'),
    path('Register/', views.register, name='register'),
    path('Dashboard/', views.dashboard, name='dashboard'),
    path('AllFarms/', views.List_farms, name='all-farms'),
    path('AllFarmers/', views.List_farmers, name='all-farmers'),
    path('AddPrices/', views.add_regional_prices, name='add-regional-prices'),
    path('FarmerDetails/<f_username>/', views.FarmerDetailsView.as_view(), name='farmer-details'),
    path('RegionalPrices/', views.RegionalPriceView.as_view(), name='regional-prices'),
    path('AllCrops/', views.CropsView.as_view(), name='all-crops'),
    path('NationalAnalysis/', NationalAnalysisView.as_view(), name='national-analysis'),
    path('ModifyRegionalPrices/<int:rp_id>/', ModifyRegionalPricesView.as_view(), name='modify-regional-prices'),
    path('FarmOutputTrends/', FarmDataAPIView.as_view(), name='farm-trends'),
    path('farm-output-trends/', FarmOutputTrendsView.as_view(), name='farm-output-trends'),
    path('DeleteRegionalPrice/<int:p_id>', views.DeleteREgionalPrice, name='delete-price'),
    path('UserProfileView/<username>/', UserProfileView.as_view(), name='user-profile')
]