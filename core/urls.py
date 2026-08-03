from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView
from inventario import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),

    path('admin/', admin.site.urls),

    path(
        'login/',
        LoginView.as_view(
            template_name='registration/login.html',
            redirect_authenticated_user=True
        ),
        name='login'
    ),

    path(
        'logout/',
        LogoutView.as_view(next_page='login'),
        name='logout'
    ),

    path('logout-beacon/', views.logout_beacon, name='logout_beacon'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('inventario.urls')),
    path('api/finance/', include('finance.urls')),
    path("", include("inventario.urls")),
]