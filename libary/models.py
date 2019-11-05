import uuid, sys
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import signals
from django.dispatch import receiver

User = get_user_model()

class AbstractBaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True

class FolderManager(models.Manager):

    def create_folder(self, folder_name, created_by):
        folder = self.model(folder_name=folder_name, created_by=created_by)
        folder.save(using=self._db)
        return folder

    def create_subfolder(self, folder_name, created_by, related_folder):
        folder = self.model(folder_name=folder_name, created_by=created_by, related_folder=related_folder)
        folder.save(using=self._db)
        return folder

    def update_folder(self, id, folder_name):
        folder = self.get(id=id)
        folder.folder_name = folder_name
        folder.save(update_fields=['folder_name', 'modified'], using=self._db)
        return folder

    def move_folder(self, id, related_folder):
        folder = self.get(id=id)
        folder.related_folder = related_folder
        folder.save(update_fields=['related_folder', 'modified'], using=self._db)
        return folder

    def promote_folder(self, id):
        folder = self.get(id=id)
        folder.related_folder = None
        folder.save(update_fields=['related_folder', 'modified'], using=self._db)
        return folder

    def change_folder_owner(self, id, created_by):
        folder = self.get(id=id)
        folder.created_by = created_by
        folder.save(update_fields=['created_by', 'modified'], using=self._db)
        return folder

    def delete_folder(self, id):
        folder = self.get(id=id)
        folder.is_deleted = 1
        folder.save(update_fields=['is_deleted', 'modified'], using=self._db)

        return folder

    def restore_folder(self, id):
        folder = self.get(id=id)
        folder.is_deleted = 0
        folder.save(update_fields=['is_deleted', 'modified'], using=self._db)

        return folder

    def restore_all(self):
        folder = self.all().filter(is_deleted=True)
        timestamp = timezone.now()
        folder.update(is_deleted=False, modified=timestamp)

        return folder

    def remove_folder(self, id):
        folder = self.get(id=id)
        folder.delete(using=self._db)
        return folder

    def remove_all(self):
        folder = self.all().filter(is_deleted=True)
        folder.delete()
        return folder

class Folder(AbstractBaseModel):
    folder_name = models.CharField(_('name'), max_length=64)
    related_folder = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name=_('created_by'))
    modified_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name=_('modified_by'))
    is_deleted = models.BooleanField(_('Is deleted'), default=False)
    folder_size = models.BigIntegerField(default=56)

    objects = FolderManager()

    def __str__(self):
        return self.folder_name

@receiver(signals.post_save, sender=Folder)
def change_owner_singal(sender, update_fields, created, instance, **kwargs):
    if created or 'created_by' in update_fields:
        childs = Folder.objects.filter(related_folder=instance.id)
        for value in childs:
            value.created_by = instance.created_by
            value.save(update_fields=['created_by', 'modified'])
    return instance
