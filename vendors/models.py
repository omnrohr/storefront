from django.db import models


class Vendor(models.Model):
    b_name = models.CharField(max_length=250, null=True, blank=True)
