from django.contrib import admin
from .models import *

# Register your models here.
# class MenuAdmin(admin.ModelAdmin):
#   list_display = ( "menuName", "price","categoryName")

class MenuAdmin(admin.ModelAdmin):
  list_display = ("menuName", "price", "categoryName")

# class OrderAdmin(admin.ModelAdmin):
#   list_display = ("table_number", "total_amount")

class OrderAdmin(admin.ModelAdmin):
  list_display = ("id", "table_number", "total_amount")

class OrderItemAdmin(admin.ModelAdmin):
  list_display =("order", "item", "quantity", "amount")

admin.site.register(Table)
admin.site.register(Category)
admin.site.register(Kitchen)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

