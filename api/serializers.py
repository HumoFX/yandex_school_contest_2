import datetime

from django.core.exceptions import ValidationError
from rest_framework import serializers
from api.models import Region, Courier, Order, Delivering


class CourierCreateSerializer(serializers.ModelSerializer):
    courier_id = serializers.IntegerField(read_only=False)
    courier_type = serializers.CharField(required=False)
    regions = serializers.ListField(required=False)
    working_hours = serializers.JSONField(required=False)
    lift_capacity = serializers.IntegerField(required=False)

    class Meta:
        model = Courier
        fields = (
            'courier_id',
            'courier_type',
            'regions',
            'working_hours',
            'lift_capacity'
        )

    def to_representation(self, instance):
        return {"id": instance}

    def validate(self, attrs):
        validation_error = ValidationError({"id": attrs.get('courier_id')})
        if Courier.objects.filter(courier_id=attrs.get('courier_id')):
            raise validation_error
        if not attrs.get('courier_type'):
            raise validation_error
        if attrs.get('courier_type') and attrs.get('courier_type') not in ('foot', 'bike', 'car'):
            raise validation_error
        if attrs.get('courier_type') in ('foot', 'bike', 'car'):
            courier_type = attrs.get('courier_type')
            lift_capacity = (courier_type == 'foot' and 10) or (courier_type == 'bike' and 15) \
                            or (courier_type == 'car' and 50)
            attrs['lift_capacity'] = lift_capacity
        if not attrs.get('working_hours'):
            raise validation_error
        if attrs.get('working_hours') and not isinstance(attrs.get('working_hours'), list):
            raise validation_error
        if not attrs.get('regions'):
            raise validation_error
        if attrs.get('regions'):
            for region in attrs.get('regions'):
                Region.objects.get_or_create(id=region)
        return attrs

    def create(self, validated_data):
        instance = super(CourierCreateSerializer, self).create(validated_data)
        return instance.courier_id


class CourierUpdateSerializer(serializers.ModelSerializer):
    courier_type = serializers.CharField(required=False)
    regions = serializers.ListField(required=False)
    working_hours = serializers.JSONField(required=False, validators=[])
    lift_capacity = serializers.IntegerField(required=False)

    class Meta:
        model = Courier
        fields = (
            'courier_id',
            'courier_type',
            'regions',
            'working_hours',
            'lift_capacity'
        )

    def to_representation(self, instance):
        regions = instance.regions.all().values_list('id', flat=True)
        response = {'courier_id': instance.courier_id, 'courier_type': instance.courier_type,
                    'regions': regions, 'working_hours': instance.working_hours}
        return response

    def validate(self, attrs):
        validation_error = ValidationError({"id": attrs.get('courier_id')})
        working_hours = attrs.get('working_hours')
        regions = attrs.get('regions')
        courier_type = attrs.get('courier_type')
        if attrs.get('courier_type'):
            if courier_type not in ('foot', 'bike', 'car'):
                raise validation_error
            elif attrs.get('courier_type') in ('foot', 'bike', 'car'):
                courier_type = attrs.get('courier_type')
                lift_capacity = (courier_type == 'foot' and 10) or (courier_type == 'bike' and 15) \
                                or (courier_type == 'car' and 50)
                attrs['lift_capacity'] = lift_capacity
        if not working_hours and working_hours is not None:
            raise validation_error
        if working_hours and not isinstance(working_hours, list):
            raise validation_error
        if not attrs.get('regions') and regions is not None:
            raise validation_error
        if regions:
            for region in attrs.get('regions'):
                Region.objects.get_or_create(id=region)
        return attrs

    def update(self, instance, validated_data):
        return super(CourierUpdateSerializer, self).update(instance, validated_data)


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(required=False)
    weight = serializers.FloatField(required=False)
    region = serializers.IntegerField(required=False)
    delivery_hours = serializers.JSONField(required=False, validators=[])

    class Meta:
        model = Order
        fields = (
            'order_id',
            'weight',
            'region',
            'delivery_hours'
        )

    def to_representation(self, list):
        response = {}
        for instance in list:
            response["id"] = instance.order_id
        return response

    def validate(self, attrs):
        validation_error = ValidationError({"id": attrs.get('order_id')})
        if Order.objects.filter(order_id=attrs.get('order_id')):
            raise validation_error
        if not attrs.get('weight'):
            raise validation_error
        if attrs.get('weight') and (attrs.get('weight') < 0.01 or attrs.get('weight') > 50):
            raise validation_error
        if not attrs.get('delivery_hours'):
            raise validation_error
        if attrs.get('delivery_hours') and not isinstance(attrs.get('delivery_hours'), list):
            raise validation_error
        if not attrs.get('region'):
            raise validation_error
        if attrs.get('region'):
            obj, created = Region.objects.get_or_create(id=attrs.get('region'))
            attrs['region'] = obj
        return attrs

    def create(self, validated_data):
        instance = super(OrderSerializer, self).create(validated_data)
        return instance.order_id


class OrderAssignSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(required=False)
    courier_id = serializers.IntegerField(required=False)

    class Meta:
        model = Delivering
        fields = (
            'order_id',
            'courier_id'
        )

    def to_representation(self, instance):
        response = {
            "orders": instance
        }
        return response

    def validate(self, attrs):
        if not Courier.objects.filter(courier_id=attrs['courier_id']):
            raise ValidationError({"id": attrs['courier_id']})
        return attrs

    def create(self, validated_data):
        courier_id = validated_data.get('courier_id')
        courier_instance = Courier.objects.get(courier_id=courier_id)
        available_orders = courier_instance.available_order()
        for order in Order.objects.filter(delivering__courier_id=courier_instance,
                                          delivering__delivered=False):
            available_orders.remove(order)
        now = datetime.datetime.now()
        if available_orders:
            for available_order in available_orders:
                Delivering.objects.create(
                    courier_id=courier_instance,
                    order_id=available_order,
                    start_time=now.strftime("%H:%M")
                )

        response = []
        for order in courier_instance.available_order():
            response.append({"id": order.order_id})
        return response


class OrderCompleteSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(required=False)
    courier_id = serializers.IntegerField(required=False)

    class Meta:
        model = Delivering
        fields = (
            'order_id',
            'courier_id'
        )

    def to_representation(self, instance):
        response = {
            "order_id": instance.order_id
        }
        return response

    def validate(self, attrs):
        validation_error = ValidationError({"id": attrs.get('order_id')})
        if not attrs.get('order_id'):
            raise validation_error
        if not attrs.get('courier_id'):
            raise validation_error
        if not Delivering.objects.filter(courier_id__courier_id=attrs.get('courier_id'),
                                         order_id__order_id=attrs.get('order_id')):
            raise validation_error
        return attrs

    def create(self, validated_data):
        deliver = Delivering.objects.get(courier_id__courier_id=validated_data.get('courier_id'),
                                         order_id__order_id=validated_data.get('order_id'))
        now = datetime.datetime.now()
        deliver.end_time = now.strftime("%H:%M")
        return deliver.order_id
