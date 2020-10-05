from django.urls import path
from .views import CreateOrderView,VerifyPaymentView,OrderDetailView

urlpatterns = [
    path("create-order/",CreateOrderView.as_view()),
    path("verify-payment/",VerifyPaymentView.as_view()),
    # below urls are under development
    path("order-detail/",OrderDetailView.as_view()),
    path("all-orders/",OrderDetailView.as_view()),
    
]