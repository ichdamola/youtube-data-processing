# comments/test_integration.py

from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from .forms import VideoForm

class VideoCommentsViewTests(TestCase):

    @patch('comments.views.fetch_video_details')
    @patch('comments.views.fetch_comments')
    def test_video_comments_post_success(self, mock_fetch_comments, mock_fetch_video_details):
        mock_fetch_video_details.return_value = {
            'title': 'Test Video',
            'description': 'Test Description',
            'view_count': '1000',
            'like_count': '100',
        }
        mock_fetch_comments.return_value = [{'author': 'Author', 'text': 'This is a comment.'}]

        response = self.client.post(reverse('video_comments'), {'video_id': 'test_video_id'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Video')
        self.assertContains(response, 'This is a comment.')

    def test_video_comments_post_no_video_id(self):
        response = self.client.post(reverse('video_comments'), {})

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': 'No video ID provided.'})

    def test_video_comments_get(self):
        response = self.client.get(reverse('video_comments'))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], VideoForm)
