from django.urls import path  # path fonksiyonunu içe aktarın
from .views import inventory_list, per_product_view, add_product, delete_inventory, update_inventory, dashboard
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from . import views
from .views import employee_list  # employee_list'i içe aktarın
from .views import inventory_list, per_product_view, add_product, delete_inventory, update_inventory, dashboard, employee_list, employee_create
from django.urls import path
from .views import signup, user_list, user_update, group_list, group_create, group_update

urlpatterns = [
    path('', inventory_list, name='inventory_list'),
    path('per_product/<int:pk>/', per_product_view, name='per_product'),
    path('add_inventory/', add_product, name='add_inventory'),
    path('delete/<int:pk>/', delete_inventory, name='delete_inventory'),
    path('update/<int:pk>/', update_inventory, name='update_inventory'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory_system/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='inventory_list'), name='logout'),
    path('employees/', employee_list, name='employee_list'),
    path('employees/create/', employee_create, name='employee_create'),
    path('signup/', signup, name='signup'),
    path('users/', user_list, name='user_list'),
    path('users/<int:pk>/update/', user_update, name='user_update'),
    path('users/', user_list, name='user_list'),  # yeni URL
    path('groups/', group_list, name='group_list'),

]
