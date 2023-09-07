import json

from django.http import JsonResponse
from requests import request, Response
from rest_framework import status

url = "https://sb2frontend-altenar2-stage.biahosted.com/api/Sportsbook/GetEventDetails?configId=12&integration=ecuabet&eventId=6855652"

# response = request("GET", url=url)
# content = json.loads(response.content.decode())
# price_content = content["Result"]["MarketGroups"][0]["Items"][0]["Items"]
# data = {}
# price_dict = {"1": None, "Draw": None, "2": None}
# for price in price_content:
#     price_dict[price["Name"]] = price["Price"]
# data["1x2"] = price_dict
# print(data)
# for price in li:
#     di[]
# print(content["Result"]["MarketGroups"][0]["Items"][0]["Items"][0]["Price"])

# MarketTypeId


def get_price_data(content_url):
    try:
        response = request("GET", url=content_url)
        content = json.loads(response.content.decode())
        price_content = content["Result"]["MarketGroups"][0]["Items"][0]["Items"]
        data = {}
        price_dict = {"1": None, "Draw": None, "2": None}
        for price in price_content:
            price_dict[price["Name"]] = price["Price"]
        data["1x2"] = price_dict
        price
    except KeyError:
        error_message = {"error": "Request Id is zero"}
        return JsonResponse(error_message, status=400)
    return data


get_price_data(url)


# class PriceDatawView(APIView):
#     def post(self, request, args, *kwargs):
#         if request.method != 'POST':
#             return JsonResponse({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#         query_params = request.query_params
#         if not query_params:
#             return JsonResponse({"Empty params": "No params provided"}, status=status.HTTP_204_NO_CONTENT)
#
#         url = query_params.get("url")
#         if not url:
#             return JsonResponse({"error": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST)
#
#         response = requests.get(url)
#         content = response.json()
#
#         price_content = content.get("Result", {}).get("MarketGroups", [])[0].get("Items", [])[0].get("Items", [])
#
#         data = {"1x2": {"1": None, "Draw": None, "2": None}}
#         for price in price_content:
#             data["1x2"][price["Name"]] = price["Price"]
#
#         return JsonResponse(data, status=status.HTTP_201_CREATED)

# content_url = "https://sb2clientstatic-altenar2-stage.biahosted.com/?skinid=ecuabet&configId=12#/live/event/112
# /6857356"
#
# response = request("GET", url=content_url)
# content = json.loads(response.content.decode())
# price_content = content["Result"]["MarketGroups"][0]["Items"][0]["Items"]
