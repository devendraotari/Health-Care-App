from consultation.models import DoctorProfile
from covidUsers.models import CustomUser
from django.http import request
from django.http import response

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.views import APIView
from settings.base import razorpay_client, RAZOR_PAY_KEY_ID, RAZOR_PAY_KEY_SECRET
from consultation.api.utils import get_request_user

from .models import Order


class CreateOrderView(APIView):
    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        user = get_request_user(request)
        context, response_status = (None, None)
        print(user.user_role.role)
        if user and user.user_role.role == "P":
            created_by_profile = user.patient
            payment_for_doctor_id = request.data.get("created_for_doctor_id", None)
            print(f"pfd{payment_for_doctor_id} type->{type(payment_for_doctor_id)}")
            try:
                payment_for_doctor = CustomUser.objects.get(
                    id=int(payment_for_doctor_id)
                )
                print(f"pfd{payment_for_doctor} type->{type(payment_for_doctor)}")
                doctor_profile = payment_for_doctor.doctor
                print(f"pfd{doctor_profile} type->{type(doctor_profile)}")
                amount = (
                    int(doctor_profile.fees) * 100
                    if doctor_profile.fees
                    else int(request.data.get("amount", 1)) * 100
                )
                print(f"amount >{amount}<")
                # amount = int(request.data.get("amount", 1)) * 100
                razorpay_order = razorpay_client.order.create(
                    {"amount": amount, "currency": "INR", "payment_capture": "1"}
                )
                order = Order(
                    status=razorpay_order["status"],
                    amount=razorpay_order["amount"],
                    amount_paid=razorpay_order["amount_paid"],
                    currency=razorpay_order["currency"],
                    entity=razorpay_order["entity"],
                    attempts=razorpay_order["attempts"],
                    receipt=razorpay_order["receipt"],
                    notes="demo note",
                    created_at=razorpay_order["created_at"],
                    created_by=created_by_profile,
                    payment_for_doctor=doctor_profile,
                )
                # order.save()
                return Response(razorpay_order, status=status.HTTP_200_OK)
            except Exception as e:
                context = {
                    "error": f"{str(e)}",
                    "msg": f"doctor not found for given Id {payment_for_doctor_id}",
                }
                response_status = status.HTTP_404_NOT_FOUND
                return Response(context, status=response_status)
        else:
            context = {"error": f"your are not authorised for this url"}
            response_status = status.HTTP_403_FORBIDDEN
            return Response(context, status=response_status)


class VerifyPaymentView(APIView):
    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        context, response_status = (None, None)
        params_dict = {
            "razorpay_order_id": request.data.get("razorpay_order_id"),
            "razorpay_payment_id": request.data.get("razorpay_payment_id"),
            "razorpay_signature": request.data.get("razorpay_signature"),
        }
        try:
            result = razorpay_client.utility.verify_payment_signature(params_dict)

            order = Order.objects.get(order_id=params_dict["razorpay_order_id"])

            return Response({"data": "Payment successfull"})
        except Exception as e:
            return Response(
                {"data": f"{str(e)}"}, status=status.HTTP_402_PAYMENT_REQUIRED
            )
'''
-------------------------------------------
Below Views are Under development
-------------------------------------------
'''
class UnpaidOrderListView(APIView):
    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        user = get_request_user(request)
        if user:
            result = razorpay_client.order.all()
            return Response(result)
        else:
            context = {"error": f"your are not authorised for this url"}
            response_status = status.HTTP_403_FORBIDDEN
            return Response(context, status=response_status)


class AllOrdersListView(APIView):
    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        user = get_request_user(request)
        if user:
            result = razorpay_client.order.all()
            return Response(result)
        else:
            context = {"error": f"your are not authorised for this url"}
            response_status = status.HTTP_403_FORBIDDEN
            return Response(context, status=response_status)


class OrderDetailView(APIView):
    permission_classes = ()
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, pk=None):
        """
        This will be used to get data of a RazorPay order
        Takes razorpay order_id as query param
        """
        context, response_status = (None, None)
        user = get_request_user(request)
        if user:
            try:
                razorpay_client.order.fetch(pk)
            except Exception as e:
                context = {"error": f"{str(e)}"}
                response_status = status.HTTP_404_NOT_FOUND
                return Response(context, status=response_status)
        else:
            context = {"error": f"your are not authorised for this url"}
            response_status = status.HTTP_403_FORBIDDEN
            return Response(context, status=response_status)




"""
<QueryDict: {'hidden': [''], 'razorpay_payment_id': ['pay_FjERpYOOvQi8xC'],
 'razorpay_order_id': ['order_FjEONx0z65aAEQ'],
 'razorpay_signature': ['958457db0527dca59a1b6c665239b741e338d1376613eb6867175d9785487145']}>
"""
