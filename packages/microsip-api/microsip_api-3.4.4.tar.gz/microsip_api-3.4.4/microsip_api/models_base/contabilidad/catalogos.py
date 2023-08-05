#encoding:utf-8
from django.db import models
from datetime import datetime

class ContabilidadCuentaContableBase(models.Model):
    id              = models.AutoField(primary_key=True, db_column='CUENTA_ID')
    nombre          = models.CharField(max_length=50, db_column='NOMBRE')
    cuenta          = models.CharField(max_length=50, db_column='CUENTA_PT')
    tipo            = models.CharField(max_length=1, db_column='TIPO')
    cuenta_padre    = models.IntegerField(db_column='CUENTA_PADRE_ID')
    
    class Meta:
        db_table = u'cuentas_co'
        abstract = True
        app_label='models_base'

    def __unicode__(self):
        return u'%s (%s)' % (self.cuenta, self.nombre)