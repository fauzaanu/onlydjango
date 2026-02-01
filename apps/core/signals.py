from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
# from .models import YourModel


# Example signal
# @receiver(post_save, sender=YourModel)
# def your_model_post_save(sender, instance, created, **kwargs):
#     """Signal handler for YourModel post_save"""
#     if created:
#         # Handle new instance creation
#         pass
#     else:
#         # Handle instance update
#         pass
