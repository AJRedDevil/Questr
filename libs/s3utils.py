# from storages.backends.s3boto import S3BotoStorage

# StaticRootS3BotoStorage = lambda: S3BotoStorage(location='questr-assets')
# MediaRootS3BotoStorage  = lambda: S3BotoStorage(location='questr-media')

from django.conf import settings
 
from storages.backends.s3boto import S3BotoStorage
 
 
StaticRootS3BotoStorage = lambda: S3BotoStorage(
    bucket=settings.AWS_STATIC_BUCKET)
 
MediaRootS3BotoStorage = lambda: S3BotoStorage(
    bucket=settings.AWS_MEDIA_BUCKET)