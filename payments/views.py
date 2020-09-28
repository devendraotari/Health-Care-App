import razorpay

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.views import APIView
from settings.base import RAZOR_PAY_KEY_ID, RAZOR_PAY_KEY_SECRET
from consultation.api.utils import get_request_user

from .models import Order


class CreateOrderView(APIView):
    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        # user = get_request_user(request)
        # print(request.data)
        # if user:
        #     pass
        amount = int(request.data.get("amount", 1000)) * 100
        client = razorpay.Client(auth=(RAZOR_PAY_KEY_ID, RAZOR_PAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": amount, "currency": "INR", "payment_capture": "1"}
        )
        order = Order(
            status=razorpay_order["status"],
            amount=razorpay_order["amount"],
            amount_paid=razorpay_order["amount_paid"],
            currency=razorpay_order['currency'],
            entity=razorpay_order['entity'],
            attempts=razorpay_order['attempts'],
            receipt=razorpay_order['receipt'],
            notes="demo note",
            created_at=razorpay_order['created_at']
        )
        return Response(razorpay_order)
