import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger('cache_metrics')


def get_all_properties():
    """
    Retrieve all properties with low-level caching.
    """
    cache_key = 'all_properties'
    
    # Try to get data from cache
    cached_properties = cache.get(cache_key)
    
    if cached_properties is not None:
        logger.info(f"Cache HIT for key: {cache_key}")
        return cached_properties
    
    # Cache miss - fetch from database
    logger.info(f"Cache MISS for key: {cache_key}")
    properties = list(Property.objects.all())
    
    # Store in cache for 1 hour (3600 seconds)
    cache.set(cache_key, properties, 3600)
    
    return properties


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache performance metrics.
    """
    try:
        redis_client = get_redis_connection('default')
        info = redis_client.info('stats')
        
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total_requests = hits + misses
        
        if total_requests > 0:
            hit_ratio = (hits / total_requests) * 100
        else:
            hit_ratio = 0.0
        
        metrics = {
            'keyspace_hits': hits,
            'keyspace_misses': misses,
            'hit_ratio': round(hit_ratio, 2),
            'total_requests': total_requests
        }
        
        logger.info(f"Redis Cache Metrics: {metrics}")
        logger.info(f"Hit Ratio: {hit_ratio:.2f}%")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'error': str(e),
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'hit_ratio': 0.0,
            'total_requests': 0
        }