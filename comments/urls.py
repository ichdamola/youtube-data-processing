from django.urls import path
from .views import video_comments

urlpatterns = [
    path('video_comments/', video_comments, name='video_comments'),
]