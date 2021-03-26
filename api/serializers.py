from rest_framework import serializers
from api.models import Region, Courier


class CourierSerializer(serializers.ModelSerializer):
    regions = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), many=True)
    working_hours = serializers.JSONField(default=[])

    class Meta:
        model = Courier
        fields = (
            'courier_id',
            'courier_type',
            'regions',
            'working_hours'
        )

    def create(self, validated_data):
        print(validated_data)

    def update(self, instance, validated_data):
        print(validated_data)
