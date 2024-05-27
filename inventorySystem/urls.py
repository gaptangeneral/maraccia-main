from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from inventory.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),  # inventory uygulamasının URL'lerini dahil etme

    # Oturum açma/kapatma işlemleri için Django'nun built-in view'larını kullanma
    path('login/', auth_views.LoginView.as_view(
        template_name='inventory_system/login.html',
        authentication_form=LoginForm  # Özel form sınıfımızı kullanma
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory_system/logout.html'), name='logout'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Sadece DEBUG modunda statik dosyaları Django üzerinden sunma

