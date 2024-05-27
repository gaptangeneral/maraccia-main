from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path("", views.inventory_list, name="inventory_list"),
    path("per_product/<int:pk>/", views.per_product_view, name="per_product"),
    path("add_inventory/", views.add_product, name="add_inventory"),
    path("delete/<int:pk>/", views.delete_inventory, name="delete_inventory"),
    path("update/<int:pk>/", views.update_inventory, name="update_inventory"),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Django'nun varsayılan giriş/çıkış URL'leri
    path("login/", auth_views.LoginView.as_view(template_name="inventory_system/login.html", authentication_form=LoginForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="inventory_system/logout.html"), name="logout"),
]
