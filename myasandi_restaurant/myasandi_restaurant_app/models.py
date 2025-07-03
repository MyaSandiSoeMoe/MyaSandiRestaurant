from django.db import models

# Create your models here.
class Table(models.Model):
    tableName = models.CharField(max_length=255)
    vacant = models.BooleanField(default=True)

    def __str__(self):
        return self.tableName
    
class Category(models.Model):
    categoryName = models.CharField(max_length=255)
    menuPhoto = models.ImageField(upload_to='photo', blank=True, null=True)

    def __str__(self):
        return self.categoryName

class Kitchen(models.Model):
    kitchenName = models.CharField(max_length=255)

    def __str__(self):
        return self.kitchenName

class Menu(models.Model):
    itemPhoto = models.ImageField(upload_to='photo')
    menuName = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField(default=0)
    categoryName = models.ForeignKey(Category, on_delete=models.CASCADE)
    kitchenName = models.ForeignKey(Kitchen, on_delete=models.CASCADE)
    out_of_order = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.menuName
    def __str__(self):
        return self.menuName

class Order(models.Model):
    table_number = models.ForeignKey(Table, on_delete=models.CASCADE)
    total_amount = models.PositiveIntegerField(default=0)
    complete_bill = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    today_date = models.DateField(auto_now_add=True)

    # def __str__(self):
    #     return self.table_number.tableName
    def __str__(self):
        return self.table_number.tableName

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    cooked_status = models.BooleanField(default=False)
    status = models.PositiveIntegerField(default=1)

class Sale(models.Model):
    table_number = models.CharField(max_length=10)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

from django.contrib.auth.models import AbstractBaseUser, User

class UserRole(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE)
    ismanager = models.BooleanField(default=False)
    iswaiter = models.BooleanField(default=False)
    iscashier = models.BooleanField(default=False)
    iskitchenStaff = models.BooleanField(default=False)



    
    
    
    
