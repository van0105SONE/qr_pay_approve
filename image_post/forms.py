from django import forms
from .models import ImagePost

class ImagePostForm(forms.ModelForm):
    class Meta:
        model = ImagePost
        fields = ["image"]