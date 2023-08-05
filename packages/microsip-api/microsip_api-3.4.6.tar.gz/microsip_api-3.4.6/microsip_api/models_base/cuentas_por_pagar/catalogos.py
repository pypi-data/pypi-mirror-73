#encoding:utf-8
from django.db import models
from datetime import datetime

class CuentasXPagarConceptoBase(models.Model):
    id                  = models.AutoField(primary_key=True, db_column='CONCEPTO_CP_ID')
    nombre_abrev        = models.CharField(max_length=30, db_column='NOMBRE_ABREV')
    crear_polizas       = models.CharField(default='N', max_length=1, db_column='CREAR_POLIZAS')
    cuenta_contable     = models.CharField(max_length=30, db_column='CUENTA_CONTABLE')
    clave_tipo_poliza   = models.CharField(max_length=1, db_column='TIPO_POLIZA')
    descripcion_poliza  = models.CharField(max_length=200, db_column='DESCRIPCION_POLIZA')

    class Meta:
        db_table = u'conceptos_cp'
        abstract = True
        app_label='models_base'

    def __unicode__(self):
        return self.nombre_abrev

class CuentasXPagarCondicionPagoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='COND_PAGO_ID')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')

    class Meta:
        db_table = u'condiciones_pago_cp'
        abstract = True
        app_label='models_base'

    def __unicode__(self):
        return self.nombre

class CuentasXPagarCondicionPagoPlazoBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='PLAZO_COND_PAG_ID')
    condicion_de_pago = models.ForeignKey('CuentasXPagarCondicionPago', db_column='COND_PAGO_ID',on_delete=models.CASCADE)
    dias = models.PositiveSmallIntegerField( db_column='DIAS_PLAZO')
    porcentaje_de_venta = models.PositiveSmallIntegerField( db_column='PCTJE_VEN')
    
    class Meta:
        db_table = u'plazos_cond_pag_cp'
        abstract = True
        app_label='models_base'

    def save(self, *args, **kwargs):    
        if self.id == -1:
            using = kwargs.get('using', None)
            using = using or router.db_for_write(CuentasXPagarCondicionPagoPlazoBase, instance=self)
            self.id = next_id('ID_CATALOGOS', using)

        super(CuentasXPagarCondicionPagoPlazoBase, self).save(*args, **kwargs)

