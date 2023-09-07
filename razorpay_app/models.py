from django.db import models
from django_extensions.db.models import TimeStampedModel


class Order(TimeStampedModel):
    razorpay_order_id = models.CharField(max_length=25)
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=5)

    def __int__(self):
        return self.pk


class Payment(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment_order')
    razorpay_payment_id = models.CharField(max_length=25)
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.razorpay_payment_id} - {self.order.id}"
