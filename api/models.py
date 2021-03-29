import datetime

from django.db import models

# Create your models here.
from django.db.models import Q


class Region(models.Model):
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return f"{self.id}"


class Courier(models.Model):
    courier_id = models.IntegerField(primary_key=True)
    courier_type = models.CharField(max_length=10)
    regions = models.ManyToManyField(Region, related_name='couriers')
    working_hours = models.JSONField()
    rating = models.FloatField(default=0)
    lift_capacity = models.IntegerField(default=0.0)

    def available_order(self):
        working_hours = list(self.working_hours)
        orders = Order.objects.filter(weight__range=(0.01, self.lift_capacity),
                                      region__in=self.regions.all(),
                                      status__in=(0, 1)
                                      ).order_by('order_id', 'weight')
        query = Q(delivering__courier_id__courier_id=self.courier_id) | \
                Q(delivering__courier_id__courier_id__isnull=True)
        orders.filter(query)
        courier_hours = []
        for working_hour in working_hours:
            courier_hours.append(working_hour.split('-'))
        available_orders = []
        total_weight = 0.0
        for order in orders:
            for delivery_hour in order.delivery_hours:
                delivery = delivery_hour.split('-')
                for courier_hour in courier_hours:
                    delivery_start = datetime.datetime.strptime(delivery[0], "%H:%M")
                    work_start = datetime.datetime.strptime(courier_hour[0], "%H:%M")
                    delivery_end = datetime.datetime.strptime(delivery[1], "%H:%M")
                    work_end = datetime.datetime.strptime(courier_hour[1], "%H:%M")
                    if delivery_start >= work_start:
                        if total_weight + order.weight <= self.lift_capacity and not available_orders.__contains__(
                                order):
                            total_weight += order.weight
                            total_weight = int(total_weight * 100) / 100
                            available_orders.append(order)
                            continue

                    elif delivery_end <= work_end:
                        if total_weight + order.weight <= self.lift_capacity and not available_orders.__contains__(
                                order):
                            total_weight += order.weight
                            total_weight = int(total_weight * 100) / 100
                            available_orders.append(order)
                            continue

        return available_orders


class Order(models.Model):
    NEW = 0
    ASSIGNED = 1
    COMPLETED = 2
    CANCELED = 3

    ORDER_STATUS = (
        (NEW, 'new'),
        (ASSIGNED, 'assigned'),
        (COMPLETED, 'completed'),
        (CANCELED, 'canceled')
    )

    order_id = models.IntegerField(primary_key=True)
    weight = models.FloatField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    delivery_hours = models.JSONField()
    status = models.IntegerField(choices=ORDER_STATUS, default=NEW)


class Delivering(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    courier_id = models.ForeignKey(Courier, on_delete=models.CASCADE)
    delivered = models.BooleanField(default=False)
    start_time = models.TimeField(verbose_name='start time', null=True, blank=True)
    end_time = models.TimeField(verbose_name='end time', null=True, blank=True)
