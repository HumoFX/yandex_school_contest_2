from rest_framework import serializers
from api.models import Region, Courier


class CourierSerializer(serializers.ModelSerializer):
    courier_id = serializers.IntegerField(read_only=False)
    regions = serializers.ListField()
    working_hours = serializers.JSONField(default=[])

    class Meta:
        model = Courier
        fields = (
            'courier_id',
            'courier_type',
            'regions',
            'working_hours'
        )

    def to_representation(self, instance):
        return {"id": instance}

    def validate_regions(self, regions):
        arr = []
        for region in regions:
            obj, created = Region.objects.get_or_create(id=region)
            arr.append(obj)
        return arr

    def create(self, validated_data):
        instance = super(CourierSerializer, self).create(validated_data)
        return instance.courier_id

    # def update(self, instance, validated_data):
    #     print(validated_data)
