from django.contrib import admin
from .models import Payment, Order, OrderProduct

# Register your models here.

#Con esta clase visualizamos en forma de tabla las características de los productos dentro de una órden
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0


#Detalle de usuarios que realizaron órdenes de compra
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_perf_page = 20
    inlines = [OrderProductInline]


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)