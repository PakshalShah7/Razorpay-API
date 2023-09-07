from rest_framework.serializers import ModelSerializer

from razorpay_app.models import Order, Payment


class OrderSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = ['razorpay_order_id', 'amount', 'currency']


class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment
        fields = ['order', 'razorpay_payment_id', 'amount', 'currency']
