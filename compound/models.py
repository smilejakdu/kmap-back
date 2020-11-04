from django.db import models

class Compound(models.Model):
    subset              = models.CharField(max_length = 250, null  = True)
    kmap_ver            = models.CharField(max_length = 250 , null = True)
    japan               = models.IntegerField(null = True)
    europe              = models.IntegerField(null = True)
    usa                 = models.IntegerField(null = True)
    nci_cancer          = models.IntegerField(null = True)
    kaichem_id          = models.CharField(max_length = 6 , null = True)
    kaipharm_chem_index = models.IntegerField(null = True)
    chem_series         = models.CharField(max_length = 50 , null = True)
    chem_series_cid     = models.CharField(max_length = 15 , null = True)
    compound            = models.CharField(max_length = 50 , null = True)
    cid                 = models.CharField(max_length = 15 , null = True)
    inchikey            = models.CharField(max_length = 27 , null = True)
    pubchem_name        = models.TextField(null = True)
    ipk                 = models.IntegerField(null = True)
    prestwick           = models.IntegerField(null = True)
    selleckchem         = models.IntegerField(null = True)
    indication          = models.CharField(max_length = 50 , null = True)
    known_target        = models.CharField(max_length = 70 , null = True)
    pathway             = models.CharField(max_length = 40 , null = True)
    synonyms            = models.TextField(null = True)
    information         = models.TextField(null = True)

    class Meta:
        db_table = "compound_info"




