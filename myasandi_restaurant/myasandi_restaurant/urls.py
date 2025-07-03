"""
URL configuration for myasandi_restaurant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from myasandi_restaurant_app.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', baseView),
    path('table/', TableView.as_view(), name='TableView'),
    path('delete/<int:pk>/', TableDelete.as_view(), name='TableDelete'),
    path('update/<int:pk>/', TableUpdate.as_view(), name='TableUpdate'),
    path('menu/', ItemView.as_view(), name='itemView'),
    path('tablePlan/', tablePlan, name='tablePlan'),
    path('orderTable/<int:pk>/', orderTable, name='orderTable'),
    path('orderTable1/<int:pk>/', orderTable1, name='orderTable1'),
    path('submit_order/', submit_order, name='submit_order'),
    path('view_order_of_table/', ViewOrderOfTable, name='view_order_of_table'),
    path('view_order_of_detail/<int:pk>/', ViewOrderofDetail, name='view_order_of_detail'),

    path('kitchen/', kitchen_display, name='kitchen_display'),

    path('mark_item_cooked/<int:pk>/', mark_item_cooked, name='mark_item_cooked'),
    path('sales_report/', sales_report, name='sales_report'),

    path('deleteCategory/<int:pk>/', deleteCategory, name='deleteCategory'),
    path('editCategory/<int:pk>/', updateCategory.as_view(), name='updateCategory'),
    path('updateMenu/<int:pk>/', updateMenu.as_view(), name='updateMenu'),
    path('deleteMenu/<int:pk>/',deleteMenu, name='deleteMenu'),
    path('add_category/', add_category, name='add_category'),
    path('add_menu/', add_menu, name='add_menu'),
    path('reset_table/<int:pk>/', reset_table, name='reset_table'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





