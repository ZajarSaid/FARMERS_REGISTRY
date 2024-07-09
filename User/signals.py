from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Sum
from itertools import groupby
from .models import Farm, Rank, OutputVerification


    
# Signal to update ranks when the total_output field is updated
# @receiver(pre_save, sender=Farm)
# def trigger_rank_update(sender, instance, **kwargs):
#     if instance.pk:  # Check if updating an existing instance
#         old_instance = Farm.objects.get(pk=instance.pk)
#         if old_instance.total_output != instance.total_output:
#             # logic behind 
#             print(old_instance.total_output)
#             print(instance.total_output)

#             # Trigger rank update if total_output has changed
#             update_ranks()


# def update_ranks():
#     # Update regional ranks
#     regional_ranks = (
#         Farm.objects.values('owner', 'region')
#         .annotate(total_output=Sum('total_output'))
#         .order_by('-total_output')
#     )
    
#     for region, farmers in groupby(regional_ranks, key=lambda x: x['region']):
#         for rank, data in enumerate(farmers, start=1):
#             farmer_id = data['owner']
#             total_output = data['total_output']
#             Rank.objects.update_or_create(
#                 farmer_id=farmer_id,
#                 defaults={'regional_rank': rank, 'region_id': region},
#             )

#     # Update national ranks
#     national_ranks = (
#         Farm.objects.values('owner')
#         .annotate(total_output=Sum('total_output'))
#         .order_by('-total_output')
#     )

#     for rank, data in enumerate(national_ranks, start=1):
#         farmer_id = data['owner']
#         total_output = data['total_output']
#         Rank.objects.update_or_create(
#             farmer_id=farmer_id,
#             defaults={'national_rank': rank},
#         )


@receiver(pre_save, sender=OutputVerification)
def trigger_rank_update(sender, instance, **kwargs):
    required_status = 'verified'

    if instance.pk:  # Check if updating an existing instance
        old_instance = OutputVerification.objects.get(pk=instance.pk)
        if old_instance.status != required_status:
            # logic behind 
            print(old_instance.status)
            

            # Trigger rank update if status has changed
            update_ranks()


def update_ranks():
    # Update regional ranks
    regional_ranks = (
        Farm.objects.values('owner', 'region')
        .annotate(total_output=Sum('total_output'))
        .order_by('-total_output')
    )
    
    for region, farmers in groupby(regional_ranks, key=lambda x: x['region']):
        for rank, data in enumerate(farmers, start=1):
            farmer_id = data['owner']
            total_output = data['total_output']
            Rank.objects.update_or_create(
                farmer_id=farmer_id,
                defaults={'regional_rank': rank, 'region_id': region},
            )

    # Update national ranks
    national_ranks = (
        Farm.objects.values('owner')
        .annotate(total_output=Sum('total_output'))
        .order_by('-total_output')
    )

    for rank, data in enumerate(national_ranks, start=1):
        farmer_id = data['owner']
        total_output = data['total_output']
        Rank.objects.update_or_create(
            farmer_id=farmer_id,
            defaults={'national_rank': rank},
        )