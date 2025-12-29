from django.contrib import admin

from order.models import ShippingAddress, Order, OrderItem

admin.site.register(ShippingAddress)
admin.site.register(OrderItem)


# Mix Order and OrderItems
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    can_delete = False
    extra = 0
    readonly_fields = ["created_at", "updated_at"]


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ("id", "status", "payment_method", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("id",)
    readonly_fields = ("payment_method", "created_at", "updated_at")


admin.site.register(Order, OrderAdmin)
