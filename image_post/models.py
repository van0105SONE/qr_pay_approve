from django.db import models

class ImagePost(models.Model):
    extracted_text =  models.TextField(blank=True) 
    image = models.ImageField(upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)
