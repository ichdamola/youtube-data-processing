# middleware.py
import logging  # Import logging
from django.core.cache import cache
from django.http import JsonResponse
from django.utils import timezone

# Configure logging
logger = logging.getLogger(__name__)

RATE_LIMIT = 5  # Number of allowed requests
TIME_WINDOW = 60  # Time window in seconds

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path == '/your-endpoint/':
            ip_address = request.META.get('REMOTE_ADDR')
            cache_key = f"rate_limit_{ip_address}"
            request_count = cache.get(cache_key, 0)
            last_request_time = cache.get(f"{cache_key}_time", timezone.now())

            # Log the current request and count
            logger.info(f"Received request from IP: {ip_address}. Current count: {request_count}")

            # Check if the time window has expired
            if (timezone.now() - last_request_time).total_seconds() > TIME_WINDOW:
                logger.info(f"Time window expired for IP: {ip_address}. Resetting request count.")
                request_count = 0  # Reset count if time window has passed

            # If request count exceeds the limit, return an error response
            if request_count >= RATE_LIMIT:
                logger.warning(f"Rate limit exceeded for IP: {ip_address}. Request denied.")
                return JsonResponse({'error': 'Rate limit exceeded. Try again later.'}, status=429)

            # Increment request count and update the last request time
            request_count += 1
            cache.set(cache_key, request_count, TIME_WINDOW)
            cache.set(f"{cache_key}_time", timezone.now(), TIME_WINDOW)
            logger.info(f"Request count updated for IP: {ip_address}. New count: {request_count}")

        response = self.get_response(request)
        return response
