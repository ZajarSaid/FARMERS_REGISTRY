from django.db import models
from Production.models import Crop, Region, District
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import FileExtensionValidator as FeV
from django.utils import timezone


# Create your models here.

EX_FILE_VALIDATOR = FeV(['csv'])
EX_IMAGE_VALIDATOR = FeV(['jpg','jpeg', 'png'])


### steps for making migrations

# 1.Make migrations for farmer model
# 2.make migrations for crop and region
# 3.make migrations for Farm
# 4.make migrations for regional prices
    


class CustomUserManager(BaseUserManager):
    def create_user(self, 
        username,
        email,
        first_name,
        last_name,
        address,
        phone,
        password=None
        ):
       
        if not email:
            raise ValueError("users must have an email")
        if not username:
            raise ValueError("users must have a username")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
             last_name=last_name,
            first_name=first_name,
            address=address,
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password
           
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
class Farmer(AbstractUser):
    STATUS = (
        ('Advancedfarmer', 'Advancedfarmer'),
        ('MediumFarmer', 'MediumFarmer'),
        ('Regular', 'Regular')
       
    )
    email = models.EmailField(verbose_name="email", unique = True)
    username = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=123, null=True)
    last_name = models.CharField(max_length=123,  null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=200, default='+255')
    status = models.CharField(max_length=200, choices=STATUS, default='MediumFarmer')
    image = models.ImageField(null=True, blank=True, upload_to='User_profile/', validators=[EX_IMAGE_VALIDATOR])
    password = models.CharField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    address = models.CharField(max_length=125)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    def get_username(self):
        return self.username
    
    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.username


class Farm(models.Model):
    name = models.CharField(max_length=123)
    size = models.CharField(max_length=123)
    crop_type = models.ForeignKey(Crop,related_name='crop_types', on_delete=models.CASCADE)
    region = models.ForeignKey(Region,related_name='regions', on_delete=models.CASCADE)
    district = models.ForeignKey(District,related_name='districtss', on_delete=models.CASCADE)
    c_s_date = models.DateTimeField()
    total_output = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Farmer, related_name='farms', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

        
    class Meta:
        verbose_name_plural = 'Farm'
    

class Rank(models.Model):
    farmer = models.OneToOneField(Farmer, on_delete=models.CASCADE)
    national_rank = models.IntegerField(null=True, blank=True)
    regional_rank = models.IntegerField(null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        verbose_name =  'Ranks'

    def __str__(self):
        return f"{self.farmer.username} - National Rank: {self.national_rank}, Regional Rank: {self.regional_rank}"

class OutputVerification(models.Model):
    STATUS = (
        ('pending', 'pending'),
        ('verified', 'verified'),
        ('denied', 'denied')
       
    )
    owner = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    farm_name = models.CharField(max_length=120)
    farm_output = models.IntegerField(null=True, blank=True)
    verification_message = models.CharField(max_length=120)
    pending_message = models.CharField(max_length=120)
    status = models.CharField(max_length=200, choices=STATUS, default='pending')
    
    def __str__(self):
        return f"{self.owner}-{self.farm_name}-Status: {self.status}"

