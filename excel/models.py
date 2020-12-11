from django.db import models


class Excel(models.Model):
    name      = models.CharField(max_length = 250)
    create_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "excels"

class Sheet(models.Model):
    name                      = models.CharField(max_length = 250 , null=True)
    Subset                    = models.CharField(max_length = 250 , null = True)
    Compound_concentration_nM = models.IntegerField(null = True)
    Replicate                 = models.CharField(max_length = 100 , null = True)
    KaiChem_ID                = models.CharField(max_length = 250 , null = True)
    Compound_Name             = models.CharField(max_length = 250 , null = True)
    Compound_treatment_time   = models.CharField(max_length = 100 , null = True)
    Cell_line                 = models.CharField(max_length = 250 , null = True)
    Plate_ID                  = models.CharField(max_length = 200 , null = True)
    Well                      = models.CharField(max_length = 100 , null = True)
    Sample_ID                 = models.CharField(max_length = 250 , null = True)
    MGI_Index_No              = models.IntegerField(null = True)
    RNA_Extraction_date       = models.CharField(max_length = 150 , null = True)
    Library_Prep_date         = models.CharField(max_length = 150 , null = True)
    Sample_sending_date_LAS   = models.CharField(max_length = 250 , null = True)
    RNA_quantity_ng           = models.IntegerField(null = True)
    DNA_quantity_ng           = models.CharField(max_length = 250, null = True)
    excel_name                = models.ForeignKey("Excel" , on_delete = models.CASCADE , null=True)
    create_at                 = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "sheets"

