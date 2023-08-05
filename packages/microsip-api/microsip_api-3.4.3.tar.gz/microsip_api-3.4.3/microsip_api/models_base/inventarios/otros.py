#encoding:utf-8
from django.db import models

class InventariosDesgloseEnDiscretosBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='DESGLOSE_DISCRETO_ID')
    docto_in_det = models.ForeignKey('InventariosDocumentoDetalle', db_column='DOCTO_IN_DET_ID',on_delete=models.CASCADE)
    art_discreto = models.ForeignKey('ArticuloDiscreto', db_column='ART_DISCRETO_ID',on_delete=models.CASCADE)
    unidades = models.IntegerField(default=0, blank=True, null=True, db_column='UNIDADES')

    class Meta:
        db_table = u'desglose_en_discretos'
        abstract = True
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.id

class InventariosDesgloseEnDiscretosIFBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='DESGL_DISCRETO_INVFIS_ID')
    docto_invfis_det = models.ForeignKey('InventariosDocumentoIFDetalle', db_column='DOCTO_INVFIS_DET_ID',on_delete=models.CASCADE)
    art_discreto = models.ForeignKey('ArticuloDiscreto', db_column='ART_DISCRETO_ID',on_delete=models.CASCADE)
    unidades = models.IntegerField(default=0, blank=True, null=True, db_column='UNIDADES')
    
    class Meta:
        db_table = u'desglose_en_discretos_invfis'
        abstract = True
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.id