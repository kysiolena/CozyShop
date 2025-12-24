from django.contrib import admin

from order.models import ShippingAddress, Order, OrderItem

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
