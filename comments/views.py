import logging  # Standard library

# Third-party libraries
from googleapiclient.discovery import build

# Django imports
from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.cache import cache

# Local application/library imports
from .forms import VideoForm

# Typing imports
from typing import Optional, List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = settings.API_KEY


def get_youtube_service() -> Any:
    return build('youtube', 'v3', developerKey=API_KEY)


def fetch_video_details(video_id: str) -> Optional[Dict[str, Any]]:
    # Try to get cached video details
    cache_key = f'video_details_{video_id}'
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        logger.info(f"Retrieved cached video details for ID: {video_id}")
        return cached_data

    try:
        youtube = get_youtube_service()
        request = youtube.videos().list(part='snippet,statistics', id=video_id)
        response = request.execute()

        if 'items' in response and response['items']:
            item = response['items'][0]
            video_details = {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'view_count': item['statistics']['viewCount'],
                'like_count': item['statistics']['likeCount'],
            }

            # Cache the video details for 5 minutes
            cache.set(cache_key, video_details, timeout=300)
            logger.info(f"Cached video details for ID: {video_id}")
            return video_details
        else:
            logger.error(f"No video found for ID: {video_id}")
            return None
    except Exception as e:
        logger.error(f"Error fetching video details for ID {video_id}: {e}")
        return None


def fetch_comments(video_id: str) -> List[Dict[str, str]]:
    # Try to get cached comments
    cache_key = f'comments_{video_id}'
    cached_comments = cache.get(cache_key)

    if cached_comments is not None:
        logger.info(f"Retrieved cached comments for video ID: {video_id}")
        return cached_comments

    youtube = get_youtube_service()
    comments: List[Dict[str, str]] = []
    next_page_token: Optional[str] = None

    try:
        while True:
            request = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                textFormat='plainText',
                pageToken=next_page_token,
            )
            response = request.execute()

            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'author': comment['authorDisplayName'],
                    'text': comment['textDisplay'],
                })

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        # Cache the comments for 5 minutes
        cache.set(cache_key, comments, timeout=300)
        logger.info(f"Cached comments for video ID: {video_id}")
    except Exception as e:
        logger.error(f"Error fetching comments for video ID {video_id}: {e}")

    return comments


@csrf_exempt
def video_comments(request: HttpRequest) -> HttpResponse:
    video_details: Optional[Dict[str, Any]] = None
    comments: List[Dict[str, str]] = []

    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        if not video_id:
            logger.warning("No video ID provided in the POST request.")
            return JsonResponse({'error': 'No video ID provided.'}, status=400)

        # Fetch video details and comments
        video_details = fetch_video_details(video_id)
        comments = fetch_comments(video_id) if video_details else []

        # Render the results in the same template
        return render(request, 'comments/video_comments.html', {
            'form': VideoForm(),
            'video_details': video_details,
            'comments': comments,
        })

    # If not a POST request, show the form
    return render(request, 'comments/video_comments.html', {'form': VideoForm()})