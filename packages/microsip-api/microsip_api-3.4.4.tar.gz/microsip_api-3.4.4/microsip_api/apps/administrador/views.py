#encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404,render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import TemplateView
from django.conf import settings
from django.db.utils import DatabaseError
# user autentication
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, AdminPasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core import management
from .models import Empresa, Registry
from microsip_api.apps.cfdi.certificador.core import CertificadorSAT
from microsip_api.apps.cfdi.core import ClavesComercioDigital


def permission_required_view(request, template_name='administrador/permission_required.html'):
    return render(request, template_name, {})

@login_required( login_url = '/login/' )
def administrador_view( request, template_name = 'administrador/main.html' ):
    """ Lista de conexiones a carpetas ( Microsip Datos ). """
    c = {}
    return render( request, template_name, c)

@login_required( login_url = '/login/' )
def empresas_view( request, template_name = 'administrador/empresas/empresas.html' ):
    c = { 'empresas' : Empresa.objects.all() }
    return render( request, template_name, c)
    
@login_required( login_url = '/login/' )
def empresa_view( request, id=None, template_name = 'administrador/empresas/empresa.html' ):
    c = { 'empresa' : Empresa.objects.get(pk=id) }
    return render( request, template_name, c)

from django.core import serializers
import json
import os
class valida_datos_facturacion(TemplateView):

    def get(self, request, *args, **kwargs):
        rfc = Registry.objects.filter(padre__nombre='DatosEmpresa').get(nombre='Rfc').get_value().replace('-','').replace(' ','')
        certificados_mal=[]
        errors= []
        
        passwords = ClavesComercioDigital("%s\\comercio_digital_claves.xlsx"%settings.EXTRA_INFO['ruta_datos_facturacion'])
        if passwords.errors:
            if not errors:
                 errors += passwords.errors

        try:
            password = passwords[rfc]
        except KeyError:
            if not errors:
                errors.append("No se encontro la contraseña en archivo [comercio_digital_claves.xlsx].")


        sellos_path = '%s\\sellos\\'%settings.EXTRA_INFO['ruta_datos_facturacion']

        if not errors:
            try:
                carpetas = os.listdir(sellos_path)
            except WindowsError:
                errors.append("No se encontro carpeta [%s]"%sellos_path)
            else:
                certificador_sat = CertificadorSAT(settings.EXTRA_INFO['ruta_datos_facturacion'])
                errors_cert = certificador_sat.certificar(empresa_folder_name= rfc)
                if errors_cert:
                    certificados_mal.append(rfc)
                    errors.append(errors_cert)



        data = {
            'certificados_mal':certificados_mal,   
            'errors':errors,
        }
        data = json.dumps(data)
        return HttpResponse(data, mimetype='application/json')

from django.db import connections
class sincronizar_basedatos(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            basedatos_activa = request.session[ 'selected_database' ]
        if basedatos_activa == '':
            return HttpResponseRedirect( '/select_db/' )
        else:
            conexion_activa_id = request.session[ 'conexion_activa' ]
            
        conexion_name = "%02d-%s"%( conexion_activa_id, basedatos_activa )
        
        # Campos nuevos en tablas
        sincronizar_tablas( conexion_name = conexion_name )

        management.call_command( 'syncdb', database = conexion_name )
        errors = []
        data = {
            'errors':errors,
        }
        data = json.dumps(data)
        return HttpResponse(data, mimetype='application/json')

def sincronizar_tablas(conexion_name):
    c = connections[ conexion_name ].cursor()
    try:
        c.execute("DELETE FROM DJANGO_CONTENT_TYPE;")
    except DatabaseError:
        pass
    else:
        import importlib

        for plugin in settings.EXTRA_APPS:
            plugin_procedures = None
            try:
                plugin_procedures_module = importlib.import_module(plugin['app']+'.procedures')
            except ImportError:
                pass
            else:
                plugin_procedures = plugin_procedures_module.procedures

            if plugin_procedures:
                for procedure in plugin_procedures.keys():
                    c.execute( plugin_procedures[procedure] )
                    c.execute('EXECUTE PROCEDURE %s;'%procedure)
                    c.execute('DROP PROCEDURE %s;'%procedure)