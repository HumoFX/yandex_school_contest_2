from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from api.views import OrderListCreateAPIView, CouriersPatchAPIView, CouriersListCreateAPIView, OrderAssignAPIView, OrderCompleteAPIView
from yandex_school_contest_2 import settings

urlpatterns = [
    path('couriers', CouriersListCreateAPIView.as_view()),
    path('couriers/<int:courier_id>', CouriersPatchAPIView.as_view()),
    path('orders', OrderListCreateAPIView.as_view()),
    path('orders/assign', OrderAssignAPIView.as_view()),
    path('orders/complete', OrderCompleteAPIView.as_view()),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

