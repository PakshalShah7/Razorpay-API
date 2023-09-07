from django.contrib import admin

from razorpay_app.models import Order, Payment

admin.site.register(Order)
admin.site.register(Payment)
