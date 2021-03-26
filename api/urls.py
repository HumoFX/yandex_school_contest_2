from django.contrib import admin
from django.urls import path
from api.views import CouriersListCreateAPIView, CouriersPatchAPIView

urlpatterns = [
    path('couriers/', CouriersListCreateAPIView.as_view()),
    path('couriers/<int:courier_id>', CouriersPatchAPIView.as_view())
]
