import json
from json import JSONDecodeError

import requests
from django.http import JsonResponse
from django.views.generic import TemplateView
from requests import request
from requests.auth import HTTPBasicAuth
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from razorpay_app.constants import ORDER_URL
from razorpay_app.models import Order
from razorpay_app.serializers import OrderSerializer
from razorpay_integration.settings import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET


# url = 'https://api.razorpay.com/v1/customers'
# data = {
#     "name": "Pakshal Shah",
#     "email": "pakshal.shah@example.com",
#     "contact": "9876543210",
# }
#
# headers = {
#     'Authorization': 'Basic ' + b64encode(bytes('rzp_test_3LLVGVG9cmu4iZ:YiUJqqhL0vehUSrTCXNbVSLy',
#                                                 'utf-8')).decode('utf-8'),
#     'Content-Type': 'application/x-www-form-urlencoded'
# }
#
# response = requests.post(url=url, data=data, headers=headers,
#                          auth=HTTPBasicAuth(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
# print(response.json())

# client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        requests.post(url=ORDER_URL, data=request.data,
                      auth=HTTPBasicAuth(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        order = Order.objects.create(amount=request.data.get('amount'),
                                     currency=request.data.get('currency'))
        order.save()
        return Response(request.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        requests.get(url=ORDER_URL, auth=HTTPBasicAuth(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        return Response(request.data, status=status.HTTP_200_OK)


class PaymentView(TemplateView):
    template_name = 'pay.html'


url = "https://sb2frontend-altenar2-stage.biahosted.com/api/Sportsbook/GetEventDetails?configId=12&integration" \
      "=ecuabet&eventId=6855652"


class PriceDataView(APIView):

    def get(self, *args, **kwargs):
        query_params = self.request.query_params

        try:
            if query_params.get("event_id"):
                event_id = query_params.get("event_id")

            elif query_params.get("url"):
                event_id = query_params.get("url").split("/")[-1]

            else:
                return Response("Please provide event id")

            content_url = "https://sb2frontend-altenar2-stage.biahosted.com/api/Sportsbook/GetEventDetails" \
                          "?configId=12&integration=ecuabet&eventId=" + event_id
            response = request("GET", url=content_url)
            content = json.loads(response.content.decode())
            market_type_id = content["Result"]["MarketGroups"][0]["Items"][0]["MarketTypeId"]
            price_content = content["Result"]["MarketGroups"][0]["Items"][0]["Items"]
            data = {"1x2": {"1": None, "Draw": None, "2": None}}

            for price in price_content:
                data["1x2"][price["Name"]] = price["Price"]

            return JsonResponse(data, status=status.HTTP_201_CREATED)
        except KeyError:
            error_message = {"error": "Invalid Request"}
            return JsonResponse(error_message, status=status.HTTP_400_BAD_REQUEST)


class PriceDatawView(APIView):
    def post(self, request, args, *kwargs):
        if request.method != 'POST':
            return JsonResponse({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        query_params = request.query_params
        if not query_params:
            return JsonResponse({"Empty params": "No params provided"}, status=status.HTTP_204_NO_CONTENT)

        url = query_params.get("url")
        if not url:
            return JsonResponse({"error": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(url)
        content = response.json()

        price_content = content.get("Result", {}).get("MarketGroups", [])[0].get("Items", [])[0].get("Items", [])

        data = {"1x2": {"1": None, "Draw": None, "2": None}}
        for price in price_content:
            data["1x2"][price["Name"]] = price["Price"]

        return JsonResponse(data, status=status.HTTP_201_CREATED)


class PriceDatasView(APIView):

    def get(self, *args, **kwargs):
        try:
            query_params = self.request.query_params
            event_id = query_params.get("event_id")
            main_url = query_params.get("url")

            if not event_id and not url:
                return Response("Please provide event id")

            if not event_id:
                event_id = main_url.split("/")[-1]

            content_url = "https://sb2frontend-altenar2-stage.biahosted.com/api/Sportsbook/GetEventDetails" \
                          "?configId=12&integration=ecuabet&eventId=" + event_id

            response = request("GET", url=content_url)
            content = json.loads(response.content.decode())
            price_content = content["Result"]["MarketGroups"][0]["Items"][0]["Items"]
            data = {"1x2": {"1": None, "Draw": None, "2": None}}
            for price in price_content:
                data["1x2"][price["Name"]] = price["Price"]
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        except KeyError:
            error_message = {"error": "Invalid Request"}
            return JsonResponse(error_message, status=status.HTTP_400_BAD_REQUEST)


class EquabetOddsView(APIView):
    "Equabet odds view"

    def get(self, *args, **kwargs):
        query_params = self.request.query_params
        try:
            if query_params.get("event_id"):
                event_id = query_params.get("event_id")
            elif query_params.get("url"):
                event_id = query_params.get("url").split("/")[-1]
            else:
                return Response({"error": "Please provide event id"})
            content_url = (
                "https://sb2frontend-altenar2-stage.biahosted.com/api/Sportsbook/GetEventDetails"
                "?configId=12&integration=ecuabet&eventId=" + event_id
            )
            response = request("GET", url=content_url)
            content = json.loads(response.content.decode())
            price_content = content["Result"]["MarketGroups"][0]["Items"][0]["Items"]
            data = {"1X2": {"1": None, "Draw": None, "2": None}}
            for price in price_content:
                data["1X2"][price["Name"]] = price["Price"]

            data["1X2"]["X"] = data["1X2"].pop("Draw")
            return Response({"odd_data": data})
        except KeyError:
            error_message = {"error": "The event has ended"}
            return Response(error_message)
        except JSONDecodeError:
            error_message = {"error": "Event id is not valid"}
            return Response(error_message)
        except Exception:
            error_message = {"error": "Something went wrong"}
            return Response(error_message)


class HtmlView(TemplateView):
    template_name = "equabet.html"


class BillView(TemplateView):
    template_name = "bill.html"
