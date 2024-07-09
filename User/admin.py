from django.contrib import admin
from .models import Farmer, Farm, Rank, OutputVerification
# Register your models here.


admin.site.register(Farmer)
admin.site.register(Farm)
admin.site.register(Rank)
admin.site.register(OutputVerification)