from django.db import models

# Create your models here.

#Plate_No Replicate_No Well_No Index_No KaiChem_ID Conc_nM Cell Time RNA_Ext_Date Lib_Prep_Date


class ExcelName(models.Model):
    name = models.CharField(max_length = 250)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "excel_names"

class ExcelSheet(models.Model):
    Plate_No      = models.IntegerField(null=True)
    Replicate_No  = models.IntegerField(null=True)
    Well_No       = models.IntegerField(null=True)
    Index_No      = models.IntegerField(default = 0)
    KaiChem_ID    = models.CharField(max_length=250, null = True , verbose_name="카이참")
    Conc_nM       = models.IntegerField(default=0)
    Cell          = models.CharField(max_length=250, null = True , verbose_name="세포")
    Time          = models.IntegerField(default=0)
    RNA_Ext_Date  = models.IntegerField(default=0)
    Lib_Prep_Date = models.IntegerField(default=0)

    def __str__(self):
        return self.KaiChem_ID

    class Meta:
        db_table = "gene_datas"




