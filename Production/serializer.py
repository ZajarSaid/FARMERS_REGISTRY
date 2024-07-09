from rest_framework import serializers
from User.models import Farm

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['crop_type', 'total_output']
