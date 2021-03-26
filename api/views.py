from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from api.serializers import CourierSerializer
from api.models import Courier, Region


# Create your views here.

class CouriersListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CourierSerializer
    queryset = Courier.objects.all()

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data['data'])
        serializer.is_valid(raise_exception=True)
        instances = self.perform_create(serializer)
        instance_serializer = CourierSerializer(instances, many=True)
        return Response(instance_serializer.data, status=status.HTTP_201_CREATED)


class CouriersPatchAPIView(generics.CreateAPIView):
    serializer_class = CourierSerializer
    queryset = Courier.objects.all()

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, *kwargs)
