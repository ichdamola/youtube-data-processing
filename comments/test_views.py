# comments/test_views.py

import unittest
from unittest.mock import patch
from .views import fetch_video_details, fetch_comments

class YouTubeAPITests(unittest.TestCase):

    @patch('comments.views.get_youtube_service')
    def test_fetch_video_details_success(self, mock_service):
        mock_response = {
            'items': [{
                'snippet': {
                    'title': 'Test Video',
                    'description': 'Test Description',
                },
                'statistics': {
                    'viewCount': '1000',
                    'likeCount': '100',
                }
            }]
        }
        mock_service().videos().list().execute.return_value = mock_response
        result = fetch_video_details('test_video_id')
        
        expected = {
            'title': 'Test Video',
            'description': 'Test Description',
            'view_count': '1000',
            'like_count': '100',
        }
        self.assertEqual(result, expected)

    @patch('comments.views.get_youtube_service')
    def test_fetch_video_details_not_found(self, mock_service):
        mock_response = {'items': []}
        mock_service().videos().list().execute.return_value = mock_response
        result = fetch_video_details('invalid_video_id')
        
        self.assertIsNone(result)

    @patch('comments.views.get_youtube_service')
    def test_fetch_comments_success(self, mock_service):
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
        mock_service().commentThreads().list().execute.return_value = mock_response
        result = fetch_comments('test_video_id')
        
        expected = [{'author': 'Author', 'text': 'This is a comment.'}]
        self.assertEqual(result, expected)

    @patch('comments.views.get_youtube_service')
    def test_fetch_comments_empty(self, mock_service):
        mock_response = {'items': []}
        mock_service().commentThreads().list().execute.return_value = mock_response
        result = fetch_comments('test_video_id')
        
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
