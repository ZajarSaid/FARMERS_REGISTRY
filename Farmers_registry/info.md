<!-- # the project has two apps

# 1. production - for managing all activies like viewing lists of farmers and adding crops regional prices as well as viewing/displaying the trends and analysis  by agricultural officers and other authenticated staffs

# 2. users - website like application where a farmer can register and create his/her own account 
    #  -->

<!-- 
### inner summary ### -->

<!-- output verification model should be with farm instance as a foregn key rather a farmer because verification process should be direct associated with a farm itself and not a farmer -->
<!-- like this 
class OutputVerification(models.Model):
    STATUS = (
        ('pending', 'pending'),
        ('verified', 'verified'),
        ('denied', 'denied')
       
    )
    farm = models.OneToOneField(Farm, on_delete=models.CASCADE)
    verification_message = models.CharField(max_length=120)
    pending_message = models.CharField(max_length=120)
    status = models.CharField(max_length=200, choices=STATUS, default='pending') -->
<!-- 
assumption in ranks generation is that a farmer will only have a single farm across the entire given period of cultivation -->