from django.contrib import admin
from api.models import Region, Courier, Order, Delivering

# Register your models here.

admin.site.register(Region)
admin.site.register(Courier)
admin.site.register(Order)
admin.site.register(Delivering)
