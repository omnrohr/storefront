from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Tag(models.Model):
    label = models.CharField(max_length=150, null=True, blank=True)


class TaggedItem(models.Model):
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    content_object = GenericForeignKey()
