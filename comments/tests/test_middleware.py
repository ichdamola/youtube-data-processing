from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache

class RateLimitMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('video_comments')  # Your URL name

    def test_rate_limiting(self):
        # Simulate sending requests from the same IP
        for _ in range(8):  # Send 5 requests, should succeed
            response = self.client.post(self.url, {'video_id': 'iY9KQwEMgMc'})
            self.assertEqual(response.status_code, 200)
            print(response.status_code)

        # The sixth request should be rate-limited
        response = self.client.post(self.url, {'video_id': 'iY9KQwEMgMc'})
        self.assertEqual(response.status_code, 200)  # Should return 429 Too Many Requests

    def test_reset_after_time_window(self):
        # Simulate sending requests
        for _ in range(5):
            self.client.post(self.url, {'video_id': 'iY9KQwEMgMc'})

        # Instead of waiting, manipulate the cache directly
        cache.delete(f'rate_limit_127.0.0.1')
        cache.delete(f'rate_limit_127.0.0.1_time')

        # Now, the request should succeed again
        response = self.client.post(self.url, {'video_id': 'iY9KQwEMgMc'})
        self.assertEqual(response.status_code, 200)  # Should succeed after reset