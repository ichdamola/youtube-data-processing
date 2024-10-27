from django import forms

class VideoForm(forms.Form):
    video_id = forms.CharField(label='YouTube Video ID', max_length=100)

