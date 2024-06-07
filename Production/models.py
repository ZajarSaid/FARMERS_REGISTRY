from django.db import models

# Create your models here.

    
class Crop(models.Model):
    STATUS = (
        ('Cash', 'Cash'),
        ('Food', 'Food')
    )
    name = models.CharField(max_length=123)
    crop_type = models.CharField(max_length=200, choices=STATUS, default='Food')
    created_at = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Crops'


class District(models.Model):
    name = models.CharField(max_length=123) 

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)



class Region(models.Model):
    name = models.CharField(max_length=23)
    districts = models.ManyToManyField(District)
    crops = models.ManyToManyField(Crop)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class RegionalPrices(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    price = models.FloatField()


    def __str__(self):
        return f'{self.crop}-{self.region}-{self.price}'