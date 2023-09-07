from django.urls import path, include
from rest_framework.routers import SimpleRouter

from razorpay_app.views import OrderView, PaymentView, EquabetOddsView, HtmlView, BillView

app_name = 'razorpay_app'

router = SimpleRouter()
router.register('order', OrderView, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('pay/', PaymentView.as_view(), name='payment'),
    path('api/', EquabetOddsView.as_view(), name='price'),
    # path('equabet/', HtmlView.as_view(), name='equabet'),
    path('bill/', BillView.as_view(), name='bill')
]
