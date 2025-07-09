import os
import environ
from django.conf import settings

env = environ.Env()

if not settings.DEBUG:
    import requests
    SUPABASE_URL = env('Supabase_URL')
    SUPABASE_SERVICE_KEY = env('Supabase_SERVICE_KEY')
    SUPABASE_BUCKET = env('Supabase_STORAGE_BUCKET')
    SUPABASE_BUCKET_CONFIDENTIAL = env('Supabase_STORAGE_BUCKET_CONFIDENTIAL')

def upload_to_supabase(file, path_in_bucket, destination):
    """
    Upload file to Supabase storage (production only).
    """
    if not hasattr(file, 'read') or not hasattr(file, 'content_type'):
        raise ValueError("Invalid file object. Pass a Django UploadedFile.")

    url = f"{SUPABASE_URL}/storage/v1/object/{destination}/{path_in_bucket}"

    headers = {
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": file.content_type
    }

    response = requests.post(url, headers=headers, data=file.read())

    if response.status_code in [200, 201]:
        return f"{SUPABASE_URL}/storage/v1/object/public/{destination}/{path_in_bucket}"
    else:
        raise Exception(f"Upload failed: {response.content.decode()}")

if settings.DEBUG:
    LOCAL_MEDIA_ROOT = env('LOCAL_MEDIA_ROOT', default='media/')  # Always define
    def save_file_locally(file, relative_path):
        """
        Save uploaded file to local filesystem during development.
        """
        full_path = os.path.join(LOCAL_MEDIA_ROOT, relative_path)

        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Use MEDIA_URL from settings to build URL path
        media_url = getattr(settings, 'MEDIA_URL', '/media/')
        return f"{media_url}{relative_path}"

def upload_to_supabase_media(file, path_in_bucket, destination=None):
    if settings.DEBUG:
        return save_file_locally(file, path_in_bucket)
    else:
        if destination is None:
            destination = SUPABASE_BUCKET
        return upload_to_supabase(file, path_in_bucket, destination)

def upload_to_supabase_confidential(file, path_in_bucket, destination=None):
    if settings.DEBUG:
        return save_file_locally(file, path_in_bucket)
    else:
        if destination is None:
            destination = SUPABASE_BUCKET_CONFIDENTIAL
        return upload_to_supabase(file, path_in_bucket, destination)
