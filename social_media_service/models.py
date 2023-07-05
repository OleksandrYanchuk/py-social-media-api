import os
import uuid

from django.db import models
from django.utils.text import slugify

from user.models import User


def image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/images/", filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(
        unique=True,
        max_length=55,
        null=False,
        blank=False,
    )
    profile_picture = models.ImageField(
        upload_to=image_file_path, null=True, blank=True
    )
    bio = models.TextField(blank=True)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    media = models.ImageField(upload_to=image_file_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
