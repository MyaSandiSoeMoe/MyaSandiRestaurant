from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView, View
from .models import *
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, get_object_or_404

from django.views.decorators.http import require_POST

import datetime
from .forms import *

# Create your views here.
def baseView(request):
    return render(request, 'base.html')

def menuView(request):
    return render(request, 'menuView.html')


class TableView(View):
    def get(self, request):

        tblList = Table.objects.all()
        context = {'tblList':tblList}
        return render(request, 'tableView.html', context)
    
    def post(self, request):
        tblname = request.POST['tblname']
        Table.objects.create(tableName= tblname)
        return redirect('/table/')
    
class TableDelete(View):
    def get(self, request, pk):
        obj = Table.objects.filter(id = pk)
        obj.delete()
        return redirect('/table/')

class TableUpdate(View):
    def get(self, request, pk):
        newtblname = request.GET['tblname']
        record = Table.objects.filter(id=int(pk))
        app = record.update(tableName= newtblname)
        return JsonResponse({'status':'success'})
    
class ItemView(View):
    def get(self, request):
        fm = CategoryModelForm()
        mfm = MenuModelForm()
        itemList = Category.objects.all()
        menuList = Menu.objects.all()
        kit = Kitchen.objects.all()
        context = {'item':itemList, 'menu':menuList, 'fm':fm, 'mfm':mfm, 'kit':kit}
        return render(request, 'menuView.html', context)

def tablePlan(request):
    tblList = Table.objects.all()
    context = {'tblList':tblList}
    return render(request, 'tablePlan.html', context)

def orderTable(request, pk):
    categoryList = Category.objects.all() 
    tbl = Table.objects.get(id=int(pk))
    context = {'category':categoryList, 'tbl':tbl}
    return render(request, 'orderTable.html', context)

def orderTable1(request, pk):
    categoryList = Category.objects.all()
    tblList = Table.objects.get(id= int(pk))
    context = {'category': categoryList, 'tbl':tblList}
    return render(request, 'orderTable1.html', context)

def submit_order(request):
    if request.method == 'POST': 
        table_number = request.POST.get('tblid') 
        item_id = request.POST.get('menuid') 
        quantity = request.POST.get('qty') 
                     
        table_obj = Table.objects.get(id=int(table_number))
        menu_obj = Menu.objects.get(id=int(item_id))

        amount_obj = int(quantity) * int(menu_obj.price)
        # print(amount_obj)

        if table_obj.vacant == True:
            order_obj = Order.objects.create(table_number = table_obj )
            order1_obj = OrderItem.objects.create(order = order_obj, item = menu_obj, quantity=quantity, 
                                              amount = amount_obj )
            table_obj.vacant = False
            table_obj.save()
            
            order_obj.total_amount += amount_obj
            order_obj.save()
        elif table_obj.vacant == False:
            table_bill = Order.objects.filter(table_number = table_obj).last()
            print(table_bill.id)
            order1_obj = OrderItem.objects.create(order = table_bill, item = menu_obj, quantity=quantity, 
                                              amount = amount_obj)
            
            table_bill.total_amount += amount_obj
            table_bill.save()
        else:
            return HttpResponse('Error')    
            # return redirect('/orderTable/'+table_number)  

            
        return redirect('/orderTable/'+table_number)  


def ViewOrderOfTable(request):
    tblList = Table.objects.all()
    context = {'tblList':tblList}
    return render(request, 'view_order_of_table.html', context)

def ViewOrderofDetail(request, pk):
    tbl_order = Table.objects.get(id=int(pk))
    
    # orderList =  Order.objects.get(table_number = tbl_order , complete_bill =False)
    orderList = Order.objects.filter(table_number=tbl_order, complete_bill=False).first()
    if not orderList:
        return render(request, 'tablePlan.html', {'tbl_order': tbl_order})


    # orderList = Order.objects.filter(table_number=tbl_order).last()

    orderitem = OrderItem.objects.filter(order= orderList)
    context = {'tbl_order':tbl_order, 'orderitem':orderitem, 'orderList':orderList}
    return render(request, 'view_order_detail.html', context)

def kitchen_display(request):
    tbl_order = OrderItem.objects.filter(cooked_status=False)
    context = {'tbl_order':tbl_order}
    return render(request, 'kitchen_display.html', context)

def mark_item_cooked(request, pk):
    item = get_object_or_404(OrderItem, id = int(pk))
    if item.status <2 :
        item.status+=1      
        item.save()
        return redirect('/kitchen/')
    else:
        item.cooked_status = True
        item.status+=1      
        item.save()
        return redirect('/kitchen/')


def sales_report(request):
    date = datetime.date.today()

    sales = Order.objects.filter(today_date=date)

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date and to_date:
        try:
            start = datetime.datetime.strptime(from_date, "%Y-%m-%d").date()
            end = datetime.datetime.strptime(to_date, "%Y-%m-%d").date()
            sales = Order.objects.filter(today_date__range=(from_date , to_date ))
        except ValueError:
            pass  # If invalid date, fall back to today
    context = {
        'sales': sales,
        'from_date': from_date,
        'to_date': to_date
    }

    
    
    context = {'sales':sales}
    return render(request, 'sales_report.html', context)
       
def deleteCategory(request, pk):
    cat_obj = Category.objects.get(id = int(pk))
    cat_obj.delete()
    return JsonResponse({'status':'success'})
    
class updateCategory(View):
    def get(self, request, pk):
        new_cat_name = request.GET['editCategoryName']
        print(new_cat_name)
        record = Category.objects.filter(id=int(pk))
        app = record.update(categoryName = new_cat_name)
        return JsonResponse({'status':'success'})

class updateMenu(View):
    def post(self, request, pk):
        new_item_photo =  request.FILES.get('photo')
        new_menu_name = request.POST['menuName']
        print(new_menu_name)
        new_price = request.POST['price']
        new_category_name = request.POST['categoryName']
        new_kitchen_name = request.POST['kitchenName']
        cat_obj = Category.objects.get(id=int(new_category_name))
        kit_obj = Kitchen.objects.get(id=int(new_kitchen_name))
        record = Menu.objects.get(id=int(pk))
        record.menuName = new_menu_name
        record.price = new_price
        record.categoryName = cat_obj
        record.kitchenName = kit_obj

            # Only update image if a new one is uploaded
        if new_item_photo:
            record.itemPhoto = new_item_photo

        record.save()

        # app = record.update(itemPhoto = new_item_photo, menuName = new_menu_name, price = new_price, categoryName = cat_obj,
        #                     kitchenName = kit_obj)
        # record.save()
        return redirect('/menu/')
    
def deleteMenu(request, pk):
    menu_obj = Menu.objects.get(id=int(pk)) 
    menu_obj.delete()  
    return JsonResponse({'status':'success'}) 

from .forms import *
def add_category(request):
    add_category_model_form = CategoryModelForm()
    if request.method == "POST":
        add_category_model_form = CategoryModelForm(request.POST, request.FILES)
        if add_category_model_form.is_valid():
            add_category_model_form.save()
            
            return redirect('/menu/')
        else:
            return HttpResponse('Error')
    return render(request, 'menuView.html', {'add_category_model_form': add_category_model_form})

def add_menu(request):
    add_menu_model_form = MenuModelForm()
    if request.method == "POST":
        add_menu_model_form = MenuModelForm(request.POST, request.FILES)
        if add_menu_model_form.is_valid():
            add_menu_model_form.save()

            return redirect('/menu/')
        else:
            return HttpResponse('Error')
    return render(request, 'menuView.html', {'add_menu_model_form':add_menu_model_form})
    
def reset_table(request, pk):
    tbl_change = Table.objects.get(id=int(pk))
    invoice_id = request.GET['invoiceId']
    order_obj = Order.objects.get(id=int(invoice_id))
    order_obj.complete_bill = True
    order_obj.save()
    tbl_change.vacant = True
    tbl_change.save()
    return JsonResponse({'status':'success'}) 

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
def loginView(request):
    if request.method == 'POST':
        usr = request.POST.get('username')
        pas = request.POST.get('password')
        usr_auth = authenticate(username = usr, password= pas)
        if usr_auth:
            login(request, usr_auth)
            return redirect('/tablePlan/')
        else:
            return redirect('/login/')
    else:
        return render(request, 'login.html')

def logoutView(request):
    logout(request)
    return redirect('/login/')
    


