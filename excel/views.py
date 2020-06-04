import json
from .models         import ExcelName , ExcelSheet
from account.utils   import login_check
from django.views    import View
from django.http     import HttpResponse, JsonResponse

from openpyxl import load_workbook
import xlrd
import re

''' 
1 )

excel_name 테이블에 엑셀을 저장한다 .

id | name |
1 | Data_gen_data | 

===========================

sheet_name 테이블에 시트 저장

id | plate_no | replicate_no | well_no | excel_name_id |
1  | 20200506 |    1         | A07     |      1        |

질문 ) sheet 이름도 저장을 해야하는지 

'''

class ExcelView(View):
    def post(self , request):
        data      = request.FILES["file"]
        sheetList = []

        try :
            if not data.name.endswith(".xlsx"):
                return JsonResponse({"message": "NOT_EXCEL_FILE"}, status=400)

            wb = load_workbook(data , data_only=True)
            for i in wb.sheetnames:
                sheetList.append(i)

            for sheet in sheetList:
                sheet_row = wb[sheet]
                print(sheet_row)
                all_values = []

                for row in sheet_row.rows:
                    row_value = []
                    for cell in row:
                        row_value.append(cell.value)
                    all_values.append(row_value)

                for n,v in enumerate(all_values):
                    if not n ==0:
                        print(v)

            return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"},status=400)

    def get(self , request):
        return

class ExcelDetailView(View):
   def post(self , request):
       return

   def delete(self , request):
       return
