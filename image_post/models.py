from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

class R2Storage(S3Boto3Storage):
    endpoint_url = 'https://5ef76ef2fdafa0e2960c1af220affe01.r2.cloudflarestorage.com/approvepayment'
    region_name = 'auto'

class ImagePost(models.Model):
    image = models.ImageField(storage=R2Storage(),upload_to="upload/")
    created_at = models.DateTimeField(auto_now_add=True)
