from django.shortcuts import get_object_or_404, render, redirect
from .models import Inventory
from django.contrib.auth.decorators import login_required
from .forms import AddInventoryForm, UpdateInventoryForm
from django.urls import reverse
from django.contrib import messages
from django_pandas.io import read_frame
import plotly.express as px
from .forms import LoginForm
from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth.models import User, Group
from .forms import CustomUserCreationForm, CustomUserChangeForm, GroupForm
from .forms import EmployeeForm
from .models import Employee

@login_required
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inventory/signup.html', {'form': form})

@login_required
def user_list(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'inventory/user_list.html', context)

@login_required
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'inventory/user_update.html', {'form': form})

@login_required
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'inventory/group_list.html', {'groups': groups})

@login_required
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'inventory/group_create.html', {'form': form})

@login_required
def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = GroupForm(instance=group)
    return render(request, 'inventory/group_update.html', {'form': form})
@login_required
def employee_list(request):
    employees = Employee.objects.all()
    context = {
        "employees": employees
    }
    return render(request, "inventory/employee_list.html", context=context)

@login_required
@login_required
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')  # veya başka bir sayfaya yönlendirin
    else:
        form = EmployeeForm()
    return render(request, 'inventory/employee_create.html', {'form': form})


@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'inventory/employee_update.html', {'form': form})

@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('employee_list')

@login_required
def logout_view(request):
    auth_views.LogoutView.as_view(next_page='/login')(request)
    return render(request, 'logout.html', {})  # logout.html şablonunu render et

@login_required
def inventory_list(request):
    inventories = Inventory.objects.all()
    context = {
        "title": "Inventory List",
        "inventories": inventories
    }
    return render(request, "inventory/inventory_list.html", context=context)

@login_required
def per_product_view(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    context = {
        'inventory': inventory
    }
    return render(request, "inventory/per_product.html", context=context)

@login_required
def add_product(request):
    if request.method == "POST":
        add_form = AddInventoryForm(data=request.POST)
        if add_form.is_valid():
            new_inventory = add_form.save(commit=False)
            new_inventory.sales = float(add_form.cleaned_data['cost_per_item']) * float(add_form.cleaned_data['quantity_sold'])
            new_inventory.save()
            messages.success(request, "Ürün Ekleme Başarılı")
            return redirect("inventory_list")
    else:
        add_form = AddInventoryForm()
    return render(request, "inventory/inventory_add.html", {"form": add_form})

@login_required
def delete_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    messages.error(request, "Ürün Silindi")
    return redirect("inventory_list")

@login_required
def update_inventory(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        updateForm = UpdateInventoryForm(data=request.POST, instance=inventory)
        if updateForm.is_valid():
            updateForm.save()
            messages.success(request, "Ürün Güncelleme Başarılı")
            return redirect("inventory_list")
    else:
        updateForm = UpdateInventoryForm(instance=inventory)
    context = {"form": updateForm}
    return render(request, "inventory/inventory_update.html", context=context)

@login_required
def dashboard(request):
    inventories = Inventory.objects.all()
    df = read_frame(inventories)

    # Satış trendi grafiği
    sales_graph = df.groupby(by="last_sale_date", as_index=False, sort=False)['sales'].sum()
    sales_graph = px.line(sales_graph, x="last_sale_date", y="sales", title="Satış Trendi", labels={"last_sale_date": "Son Satış Tarihi", "sales": "Toplam Satış"})
    sales_graph = sales_graph.to_html(full_html=False, include_plotlyjs=False)

    # En çok satan ürün grafiği
    best_performing_product_df = df.groupby(by="name").sum().sort_values(by="quantity_sold", ascending=False)
    best_performing_product = px.bar(
        best_performing_product_df,
        x=best_performing_product_df.index,
        y='quantity_sold',
        title="En Çok Satan Ürün",
        labels={"x": "Ürün Adı", "quantity_sold": "Satılan Adet"}
    )
    best_performing_product = best_performing_product.to_html(full_html=False, include_plotlyjs=False)

    # Stokta en çok bulunan ürün grafiği
    most_product_in_stock_df = df.groupby(by="name").sum().sort_values(by="quantity_in_stock", ascending=False)
    most_product_in_stock = px.pie(
        most_product_in_stock_df,
        names=most_product_in_stock_df.index,
        values=most_product_in_stock_df.quantity_in_stock,
        title="Stokta En Çok Bulunan Ürün",
        labels={"names": "Ürün Adı", "values": "Stok Adedi"}
    )
    most_product_in_stock = most_product_in_stock.to_html(full_html=False, include_plotlyjs=False)

    context = {
        "sales_graph": sales_graph,
        "best_performing_product": best_performing_product,
        "most_product_in_stock": most_product_in_stock
    }
    return render(request, "inventory/dashboard.html", context=context)
