from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from api.serializers import CourierSerializer
from api.models import Courier, Region


# Create your views here.

class CouriersListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CourierSerializer
    queryset = Courier.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data['data'], many=isinstance(request.data['data'], list))
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"couriers": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response()


class CouriersPatchAPIView(generics.CreateAPIView):
    serializer_class = CourierSerializer
    queryset = Courier.objects.all()

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, *kwargs)
