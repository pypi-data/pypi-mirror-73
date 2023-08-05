# from django.conf.urls import patterns, url, include
from django.urls import path,include
from .views import valida_datos_facturacion, sincronizar_basedatos, permission_required_view
from microsip_api.apps.administrador import views
urlpatterns = (
	path('',views.administrador_view),
	path('empresas/',views.empresas_view),
	path('empresa/<int:id>/',views.empresa_view),
	path('valida_datos_facturacion/', valida_datos_facturacion.as_view()),
	path('permission_required/', permission_required_view),
	path('sincronizar_basedatos/', sincronizar_basedatos.as_view()),
	path('', include('microsip_api.apps.administrador.modules.sucursales.urls')),
	path('', include('microsip_api.apps.administrador.modules.usuarios.urls')),
)