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


urlpatterns = [
    # ... diğer URL yapılandırmaları
    path("login/", auth_views.LoginView.as_view(template_name="inventory_system/login.html", authentication_form=LoginForm), name="login"),
    # ... diğer URL yapılandırmaları
]

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
