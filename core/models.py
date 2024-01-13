from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("Created time"),
                                      help_text=_("Created at this time"))
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("Modified time"),
                                      help_text=_("Modified at this time"))

    class Meta:
        abstract = True


class LogicalQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_deleted=True)

    def hard_delete(self):
        return super().delete()


class LogicalManager(models.Manager):
    def get_queryset(self):
        return LogicalQuerySet(self.model).filter(is_deleted=False, is_active=True)

    def all_objects(self):
        return LogicalQuerySet(self.model)

    def deleted(self):
        return LogicalQuerySet(self.model).filter(is_deleted=True)


class LogicalBaseModel(models.Model):
    is_active = models.BooleanField(default=True, verbose_name=_("Active status"),
                                    help_text=_("This is active status"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("Status: Deleted"),
                                     help_text=_("Status is deleted"))

    objects = LogicalManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super().delete()

    def restore(self):
        self.is_deleted = False
        self.save()
