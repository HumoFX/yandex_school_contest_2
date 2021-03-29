from rest_framework import generics, status
from rest_framework.response import Response
from api.serializers import CourierCreateSerializer, CourierUpdateSerializer, OrderSerializer, OrderAssignSerializer, \
    OrderCompleteSerializer
from api.models import Courier, Region, Order, Delivering


# Create your views here.


class CouriersListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CourierCreateSerializer
    queryset = Courier.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data['data'], many=isinstance(request.data['data'], list))
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"couriers": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            err_list = []
            for err in serializer.errors:
                if err:
                    err_list.append({"id": int(err['id'][0])})
            return Response({"validation_error": {"couriers": err_list}}, status=status.HTTP_400_BAD_REQUEST)


class CouriersPatchAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CourierUpdateSerializer
    queryset = Courier.objects.all()
    lookup_url_kwarg = 'courier_id'

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, *kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data['data'], many=isinstance(request.data['data'], list))
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"orders": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            err_list = []
            for err in serializer.errors:
                if err:
                    err_list.append({"id": int(err['id'][0])})
            return Response({"validation_error": {"orders": err_list}}, status=status.HTTP_400_BAD_REQUEST)


class OrderAssignAPIView(generics.ListCreateAPIView):
    serializer_class = OrderAssignSerializer
    queryset = Delivering.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"orders": serializer.data['orders']}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderCompleteAPIView(generics.ListCreateAPIView):
    serializer_class = OrderCompleteSerializer
    queryset = Delivering.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
