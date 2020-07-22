import xlrd
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kmap_info_back.settings')
import django
django.setup()
from compound.models             import Compound

workbook = xlrd.open_workbook("kmap_info.xlsx")
worksheet = workbook.sheet_by_name("Sheet 1")
total_list = worksheet._cell_values
result_list = []

for xr in total_list[1:]:
    result_list.append(xr)

for row in result_list:
    Compound.objects.create(
        subset              = row[0],
        kmap_ver            = row[1],
        japan               = int(row[2]),
        europe              = int(row[3]),
        usa                 = int(row[4]),
        nci_cancer          = int(row[5]),
        kaichem_id          = row[6],
        kaipharm_chem_index = int(row[7]),
        chem_series         = row[8],
        chem_series_cid     = row[9],
        compound            = row[10],
        cid                 = row[11],
        inchikey            = row[12],
        pubchem_name        = row[13],
        ipk                 = int(row[14]),
        prestwick           = int(row[15]),
        selleckchem         = int(row[16]),
        indication          = row[17],
        known_target        = row[18],
        pathway             = row[19],
        synonyms            = row[20],
        information         = row[21],
    )

print("=" * 100)
