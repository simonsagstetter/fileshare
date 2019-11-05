import uuid, os
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import get_user_model
from fileshare import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.db.models import signals
from django.dispatch import receiver

User = get_user_model()

from libary.models import AbstractBaseModel, Folder

fs = FileSystemStorage(
location=settings.MEDIA_ROOT,
base_url=settings.MEDIA_URL,
file_permissions_mode=None,
directory_permissions_mode=None,
)

def get_upload_path(instance, filename):
    created_by = str(instance.created_by.email)
    date = str(timezone.localdate())
    encrypted_filename = '{0}{1}'.format(uuid.uuid4(), filename)
    path = 'user_{0}/{1}/{2}'.format(created_by, date, encrypted_filename)
    return path


class FileManager(models.Manager):

    def upload_file(self, real_filename, upload_file, related_folder, created_by):
        if related_folder is None:
            obj = self.model(real_filename=real_filename, upload_file=upload_file, created_by=created_by)
            obj.save(using=self._db)
            return obj
        else:
            obj = self.model(real_filename=real_filename, upload_file=upload_file, created_by=created_by, related_folder=related_folder)
            obj.save(using=self._db)
            return obj

    def update_file(self, id, real_filename):
        file = self.get(id=id)
        file.real_filename = real_filename
        file.save(update_fields=['real_filename', 'modified'], using=self._db)
        return file

    def delete_file(self, id):
        file = self.get(id=id)
        file .is_deleted = 1
        file .save(update_fields=['is_deleted', 'modified'], using=self._db)
        return file

    def restore_file(self, id):
        file = self.get(id=id)
        file.is_deleted = 0
        file.save(update_fields=['is_deleted', 'modified'], using=self._db)
        return file

    def restore_all(self):
        file = self.all().filter(is_deleted=True)
        timestamp = timezone.now()
        file.update(is_deleted=False, modified=timestamp)
        return file

    def remove_all(self):
        file = self.all().filter(is_deleted=True)
        for value in file:
            storage, path = value.upload_file.storage, value.upload_file.path
            storage.delete(path)
        file.delete()
        return file

class File(AbstractBaseModel):
    upload_file = models.FileField(upload_to=get_upload_path,storage=fs)
    real_filename = models.CharField(_('real filename'), max_length=128, default='')
    related_folder = models.ForeignKey(Folder, null=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name=_('file_created_by'))
    modified_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name=_('file_modified_by'))
    is_deleted = models.BooleanField(_('Is deleted'), default=False)

    objects = FileManager()

    def __str__(self):
        return self.upload_file.name

@receiver(signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.upload_file:
        if os.path.isfile(instance.upload_file.path):
            os.remove(instance.upload_file.path)
