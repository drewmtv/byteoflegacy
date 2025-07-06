import requests
import os

SUPABASE_URL = os.environ.get('Supabase_URL')
SUPABASE_SERVICE_KEY = os.environ.get('Supabase_SERVICE_KEY')
SUPABASE_BUCKET = os.environ.get('Supabase_STORAGE_BUCKET')
SUPABASE_BUCKET_CONFIDENTIAL = os.environ.get('Supabase_STORAGE_BUCKET_CONFIDENTIAL')

def upload_to_supabase_media(file, path_in_bucket, destination=SUPABASE_BUCKET):
    return upload_to_supabase(file, path_in_bucket, destination)

def upload_to_supabase_confidential(file, path_in_bucket, destination=SUPABASE_BUCKET_CONFIDENTIAL):
    return upload_to_supabase(file, path_in_bucket, destination)

def upload_to_supabase(file, path_in_bucket, destination):
    """
    Uploads a file to Supabase Storage using REST API.
    """
    # Validate that we have a real file object
    if not hasattr(file, 'read') or not hasattr(file, 'content_type'):
        raise ValueError("Invalid file object. Ensure you're passing a Django UploadedFile.")

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
