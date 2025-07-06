from django.core.exceptions import ValidationError

def validate_image_file(file, max_size_mb=2):
    if not file.content_type.startswith('image/'):
        raise ValidationError("Uploaded file must be an image.")
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Image must be under {max_size_mb}MB.")
