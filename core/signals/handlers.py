from django.conf import settings
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from core.models import *
from store.models import Cart,WishList

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_Profile_for_new_user(sender, **kwargs):
  if kwargs['created']:
      print(kwargs['created'])
      print(kwargs['instance'])
      print(kwargs['instance'].profile_type)
      if kwargs['instance'].profile_type == 'PAT':
        patient = Patient.objects.create(user=kwargs['instance'])
        Cart.objects.create(customer=patient)
        WishList.objects.create(customer=patient)
      elif kwargs['instance'].profile_type == 'DR':
        Doctor.objects.create(user=kwargs['instance'])


@receiver(post_delete, sender=PersonImage)
def delete_image_file(sender, instance, **kwargs):
    """
    Deletes the image file from the file system when the Image object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)