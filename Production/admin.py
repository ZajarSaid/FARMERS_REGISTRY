from django.contrib import admin
from .models import District, Region, Crop, RegionalPrices
# Register your models here.


admin.site.register(District)
admin.site.register(Crop)
admin.site.register(Region)
admin.site.register(RegionalPrices)