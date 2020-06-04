from django.db import models


class ExcelTable(models.Model):
    name = models.CharField(max_length = 250)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "excel_tables"

class SheetTable(models.Model):
    sheet_name    = models.CharField(max_length=250 , null=True)
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
    excel_name    = models.ForeignKey("ExcelTable" , on_delete = models.CASCADE , null = True)

    def __str__(self):
        return self.KaiChem_ID

    class Meta:
        db_table = "sheet_tables"

