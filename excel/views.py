import json
from .models         import ExcelTable ,SheetTable
from account.utils   import login_check
from django.views    import View
from django.http     import HttpResponse, JsonResponse

from openpyxl import load_workbook
import xlrd


class ExcelView(View):
    def post(self , request):
        data      = request.FILES["file"]
        sheetList = []
        excel_name = str(data)


        try :
            if not data.name.endswith(".xlsx"):
                return JsonResponse({"message": "NOT_EXCEL_FILE"}, status=400)

            if ExcelTable.objects.filter(name = excel_name):
                return JsonResponse({"message" : "EXISTS_EXCEL"}, status=400)

            ExcelTable(
                name = excel_name
            ).save()

            wb = load_workbook(data , data_only=True)
            [sheetList.append(i) for i in wb.sheetnames]

            for sheet in sheetList:
                sheet_row  = wb[sheet]
                all_values = []

                for row in sheet_row.rows:
                    row_value = []
                    [row_value.append(cell.value) for cell in row]
                    all_values.append(row_value)

                for num , values in enumerate(all_values):
                    if not num ==0:


                        SheetTable.objects.create(
                            sheet_name    = sheet,
                            Plate_No      = values[0],
                            Replicate_No  = values[1],
                            Well_No       = values[2],
                            Index_No      = values[3],
                            KaiChem_ID    = values[4],
                            Conc_nM       = values[5],
                            Cell          = values[6],
                            Time          = values[7],
                            RNA_Ext_Date  = values[8],
                            Lib_Prep_Date = values[9],
                            Seq_Req_Date  = values[10],
                            NGS_Data_Date = values[11],
                            excel_name_id = ExcelTable.objects.get(name = excel_name).id
                        )

            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"},status=400)

    def get(self , request):
        return

class ExcelDetailView(View):
   def post(self , request):
       return

   def delete(self , request):
       return
