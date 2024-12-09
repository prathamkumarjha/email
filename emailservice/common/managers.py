import logging
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Configure logging
logger = logging.getLogger(__name__)

class DefaultManager(models.Manager):

    def get_object(self, **kwargs):
        """
        Retrieve a single object based on the provided criteria.
        Raises a DoesNotExist exception if no object is found.
        """
        try:
            obj = self.get_queryset().get(**kwargs)
            logger.error(f"Retrieved object: {obj} with criteria: {kwargs}")
            return obj
        except self.model.DoesNotExist:
            logger.error(f"{self.model.__name__} matching query does not exist with criteria: {kwargs}")
            raise self.model.DoesNotExist(f"{self.model.__name__} matching query does not exist.")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def create(self, *args, **kwargs):
        
        obj = super().create(*args, **kwargs)
        logger.error(f"Created object: {obj} with args: {args}, kwargs: {kwargs}")
        return obj

    def update(self, *args, **kwargs):
        count = super().update(*args, **kwargs)
        logger.error(f"Updated {count} objects with args: {args}, kwargs: {kwargs}")
        return count

    # def soft_delete(self, instance):
    #     logger.error(f"Soft delete called for model: {self.model} with ")
    #     instance.is_active = False
    #     instance.save()

    def force_delete(self):
        count = super().delete()
        logger.error(f"Force deleted {count} objects")
        return count

    def saves(self, instance, *args, **kwargs):
        """
        Save an instance of the model, handling both creation and update.
        """
        print("_)____________________________________________________hello____________")
        # user = self._get_current_user()
        # if not instance.pk:
            # New instance
            # if hasattr(instance, 'created_by') and not instance.created_by:
            #     instance.created_by = user
            # logger.error(f"Saving new instance: {instance}")
        # else:
            # Existing instance
            # if hasattr(instance, 'updated_by'):
            #     instance.updated_by = user
            # logger.error(f"Updating instance: {instance}")

        instance.save(*args, **kwargs)
        logger.error(f"Saved instance: {instance}")
        return instance
    # def _get_current_user(self):
    #     from django.contrib.auth.models import AnonymousUser
    #     from django.contrib.auth import get_user_model
        
    #     User = get_user_model()

    #     try:
    #         user = getattr(self._get_request(), "user", None)
    #         if user and isinstance(user, User):
    #             return user
    #     except:
    #         pass
    #     return None

    def _get_request(self):
        from django.core.exceptions import AppRegistryNotReady

        try:
            from django.contrib.auth.middleware import get_user
            from django.contrib.auth.models import AnonymousUser
            from threading import local

            _thread_locals = local()
            return getattr(_thread_locals, "request", None)
        except AppRegistryNotReady:
            return None


class ActiveManager(DefaultManager):
    def get_queryset(self):
        return super().get_queryset().filter(retry__lt=10).exclude(status='sent')

class BaseManager(DefaultManager):
    def get_queryset(self):
        return super().get_queryset().filter(retry__lt=10).exclude(status='sent')



class InactiveManager(DefaultManager):
    def get_queryset(self):
        return super().get_queryset().filter(retry__gt=10).exclude(status='sent')
