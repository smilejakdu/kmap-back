import xlrd
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'kmap_info_back.settings')
import django
django.setup()
from compound.models             import Compound

workbook    = xlrd.open_workbook("kmap_info.xlsx")
worksheet   = workbook.sheet_by_name("Sheet 1")
total_list  = worksheet._cell_values
result_list = []

for xr in total_list[1:]:
    result_list.append(xr)

for row in result_list:
    Compound.objects.create(
        subset              = row[1],
        kmap_ver            = row[2],
        japan               = int(row[3]),
        europe              = int(row[4]),
        usa                 = int(row[5]),
        nci_cancer          = int(row[6]),
        kaichem_id          = row[7],
        kaipharm_chem_index = int(row[8]),
        chem_series         = row[9],
        chem_series_cid     = row[10],
        compound            = row[11],
        cid                 = row[12],
        inchikey            = row[13],
        pubchem_name        = row[14],
        ipk                 = int(row[15]),
        prestwick           = int(row[16]),
        selleckchem         = int(row[17]),
        indication          = row[18],
        known_target        = row[19],
        pathway             = row[20],
        synonyms            = row[21],
        information         = row[22],
    )

print("=" * 100)
