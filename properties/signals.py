import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

logger = logging.getLogger('cache_metrics')


@receiver(post_save, sender=Property)
def invalidate_cache_on_save(sender, instance, created, **kwargs):
    """
    Invalidate the all_properties cache when a Property is created or updated.
    """
    cache_key = 'all_properties'
    cache.delete(cache_key)
    
    action = "created" if created else "updated"
    logger.info(f"Property {instance.id} was {action}. Cache key '{cache_key}' invalidated.")


@receiver(post_delete, sender=Property)
def invalidate_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate the all_properties cache when a Property is deleted.
    """
    cache_key = 'all_properties'
    cache.delete(cache_key)
    
    logger.info(f"Property {instance.id} was deleted. Cache key '{cache_key}' invalidated.")