from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView


from inventario import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout-beacon/', views.logout_beacon, name='logout_beacon'),

    # Evitar login duplicado: redirigir las rutas por defecto de 'accounts/'
    path(
        'accounts/login/',
        RedirectView.as_view(pattern_name='login', permanent=False),
    ),
    path(
        'accounts/logout/',
        RedirectView.as_view(pattern_name='logout', permanent=False),
    ),

    path('accounts/', include('django.contrib.auth.urls')),

    path('login/', views.LoginConPerfilesView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('', include('inventario.urls')),
    path('api/finance/', include('finance.urls')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )