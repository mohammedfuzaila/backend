from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.utils.deconstruct import deconstructible
from urllib.parse import quote

@deconstructible
class DatabaseStorage(Storage):
    def _save(self, name, content):
        from api.models import MediaFile
        file_content = content.read()
        content_type = getattr(content, 'content_type', 'application/octet-stream')
        # On Render, files get re-uploaded when they are changed in the admin
        MediaFile.objects.update_or_create(
            name=name,
            defaults={'content': file_content, 'content_type': content_type}
        )
        return name

    def _open(self, name, mode='rb'):
        from api.models import MediaFile
        try:
            f = MediaFile.objects.get(name=name)
            return ContentFile(f.content, name=name)
        except MediaFile.DoesNotExist:
            return None

    def exists(self, name):
        from api.models import MediaFile
        return MediaFile.objects.filter(name=name).exists()

    def url(self, name):
        # We serve it via a custom view
        return f'/api/media/{quote(name)}'
