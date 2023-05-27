import os

from medicines.models import Image
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.conf import settings


@receiver(post_delete, sender=Image)
def delete_image_file(sender, instance, **kwargs):
    """
    Deletes the image file from the file system when the Image object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)