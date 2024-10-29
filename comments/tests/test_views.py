import unittest
from django.core.cache import cache
from django.test import TestCase
from unittest.mock import patch
from comments.views import fetch_comments

class YouTubeAPITests(TestCase):
    def setUp(self):
        # Clear the cache before each test
        cache.clear()

    @patch('comments.views.get_youtube_service')
    def test_fetch_comments_success(self, mock_service):
        # Setup the mock response for comments
        mock_response = {
            'items': [{
                'snippet': {
                    'topLevelComment': {
                        'snippet': {
                            'authorDisplayName': 'Author',
                            'textDisplay': 'This is a comment.'
                        }
                    }
                }
            }]
        }
        # Mock the `execute` method to return the mock response
        mock_service().commentThreads().list().execute.return_value = mock_response
        
        # Call the function to fetch comments
        result = fetch_comments('test_video_id')

        # Expected output
        expected = [{'author': 'Author', 'text': 'This is a comment.'}]
        
        print(f"Fetched comments: {result}")  # Debugging output to see what was fetched
        self.assertEqual(result, expected)  # Ensure it matches expected output

    @patch('comments.views.get_youtube_service')
    def test_fetch_comments_empty(self, mock_service):
        mock_response = {'items': []}
        mock_service().commentThreads().list().execute.return_value = mock_response
        
        result = fetch_comments('test_video_id')
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()