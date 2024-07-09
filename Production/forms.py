from django import forms
from .models import RegionalPrices
from .models import Region


class UpdateFarmForm(forms.Form):
    name = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Farm Name'})
    output = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Output'})



class MarketPriceForm(forms.ModelForm):

    class Meta:
        model = RegionalPrices
        fields = ('region', 'crop', 'price')

        widgets = {
                
                'crop':forms.Select(attrs={'class':'form-control', 'placeholder':'Crop'}),
                'price':forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter price'}),   
                'region':forms.Select(attrs={'class':'form-control', 'placeholder':'Enter region'}),
            }



class RegionFilterForm(forms.Form):
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False, label='Select Region')

