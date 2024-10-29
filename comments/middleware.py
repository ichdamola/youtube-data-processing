# middleware.py
import logging
from django.core.cache import cache
from django.http import JsonResponse
from django.utils import timezone

# Set up logging
logger = logging.getLogger(__name__)

RATE_LIMIT = 2  # Number of allowed requests
TIME_WINDOW = 60  # Time window in seconds

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path == '/video_comments/':
            ip_address = request.META.get('REMOTE_ADDR')
            cache_key = f"rate_limit_{ip_address}"
            request_count = cache.get(cache_key, 0)
            last_request_time = cache.get(f"{cache_key}_time", timezone.now())

            # Check if the time window has expired
            if (timezone.now() - last_request_time).total_seconds() > TIME_WINDOW:
                logger.info(f"Rate limit reset for IP: {ip_address}")
                request_count = 0  # Reset count if time window has passed

            # If request count exceeds the limit, return an error response
            if request_count >= RATE_LIMIT:
                logger.warning(f"Rate limit exceeded for IP: {ip_address}")
                return JsonResponse({'error': 'Rate limit exceeded. Try again later.'}, status=429)

            # Increment request count and update the last request time
            request_count += 1
            cache.set(cache_key, request_count, TIME_WINDOW)
            cache.set(f"{cache_key}_time", timezone.now(), TIME_WINDOW)
            logger.info(f"Request count for IP: {ip_address} is now {request_count}")

        response = self.get_response(request)
        return response