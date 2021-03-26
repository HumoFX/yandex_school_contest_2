from django.db import models


# Create your models here.
class Region(models.Model):
    id = models.IntegerField(primary_key=True)


class Courier(models.Model):
    courier_id = models.IntegerField(primary_key=True)
    courier_type = models.CharField(max_length=10)
    regions = models.ManyToManyField(Region, related_name='couriers')
    working_hours = models.JSONField(default=[])
