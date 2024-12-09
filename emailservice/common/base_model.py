from django.db import models
from django.conf import settings
from .managers import BaseManager, ActiveManager, InactiveManager, DefaultManager

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    objects = BaseManager()
    all_objects = DefaultManager()
    active_objects = ActiveManager()
    inactive_objects = InactiveManager()
    class Meta:
        abstract = True