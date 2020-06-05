from django.db import models


class Excel(models.Model):
    name = models.CharField(max_length = 250)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "excels"

class ExcelTest(models.Model):
    file_name = models.FileField(upload_to=Excel)

class Sheet(models.Model):
    name    = models.CharField(max_length=250 , null=True)
    Plate_No      = models.IntegerField(null=True)
    Replicate_No  = models.IntegerField(null=True)
    Well_No       = models.CharField(max_length=250 , null=True)
    Index_No      = models.IntegerField(default = 0)
    KaiChem_ID    = models.CharField(max_length=250, null = True , verbose_name="카이참")
    Conc_nM       = models.IntegerField(default=0)
    Cell          = models.CharField(max_length=250, null = True , verbose_name="세포")
    Time          = models.IntegerField(default=0)
    RNA_Ext_Date  = models.IntegerField(default=0)
    Lib_Prep_Date = models.IntegerField(default=0)
    Seq_Req_Date  = models.IntegerField(default=0)
    NGS_Data_Date = models.IntegerField(default=0)
    excel_name    = models.ForeignKey("Excel" , on_delete = models.CASCADE , null = True)

    def __str__(self):
        return self.KaiChem_ID

    class Meta:
        db_table = "sheets"

