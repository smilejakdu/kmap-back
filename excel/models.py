from django.db import models


class Excel(models.Model):
    name      = models.CharField(max_length = 250)
    create_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "excels"

class Sheet(models.Model):
    name                = models.CharField(max_length=250 , null=True)
    Subset              = models.CharField(max_length = 250 , null = True)
    Concentration_nM    = models.IntegerField(null    = True)
    Replicate_No        = models.CharField(max_length  = 250 , null = True)
    KaiChem_ID          = models.CharField(max_length = 250 , null = True)
    Cell                = models.CharField(max_length = 250 , null = True)
    Treat_Time          = models.CharField(max_length = 250 , null = True)
    Well_Location       = models.CharField(max_length = 250 , null = True)
    Index_No            = models.CharField(max_length = 250 , null = True)
    Seeding_Date        = models.IntegerField(null = True)
    RNA_Extraction_Date = models.IntegerField(null = True)
    Library_Prep_Date   = models.IntegerField(null = True)
    Seq_Request_Date    = models.IntegerField(null = True)
    NGS_Data_Date       = models.IntegerField(null = True)
    excel_name          = models.ForeignKey("Excel" , on_delete=models.CASCADE , null=True)
    create_at           = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "sheets"

