import json
from .models         import Excel ,Sheet
from account.utils   import login_check
from django.views    import View
from django.http     import HttpResponse, JsonResponse
from openpyxl        import load_workbook
import xlrd


class ExcelView(View):
    def post(self , request):
        data       = request.FILES["file"]
        sheetList  = []
        excel_name = str(data)

        try :
            if not data.name.endswith(".xlsx"):
                return JsonResponse({"message": "NOT_EXCEL_FILE"}, status=400)

            if Excel.objects.filter(name = excel_name).exists():
                return JsonResponse({"message" : "EXISTS_EXCEL"}, status=400)

            Excel(
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


                        Sheet.objects.create(
                            name          = sheet,
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
                            excel_name_id = Excel.objects.get(name = excel_name).id
                        )

            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"},status=400)

    def get(self , request): 
        try:
            query = request.GET.get('keyword', None)  

            if query:
                excel_search = Excel.objects.filter(name__icontains = query).all()
                excel_data = [{
                    "id"   : excel.id,
                    "name" : excel.name
                }for excel in excel_search]

                return JsonResponse({"data" : excel_data} , status=200)

            excel_data = (Excel.
                          objects.
                          all().
                          values())
            excel_count = Excel.objects.count()

            return JsonResponse({"data": {
                "excel_data"  : list(excel_data),
                "excel_count" : excel_count
            }}, status=200)

        except KeyError:
            return JsonResponse({"message","INVALID_KEY"} , status=400)

        except TypeError:
            return JsonResponse({"message":"INVALID_TYPE"} , status=400)

        except Excel.DoesNotExist:
            return JsonResponse({"message":"DOESNOT_EXCEL"},status=400)


class ExcelDetailView(View):
    def get(self, request , excel_name): 

        if not Excel.objects.filter(name=excel_name).exists():
            return JsonResponse({"message": "DOESNOT_EXCEL"}, status=400)

        try:
            sheet_name = (Excel.
                          objects.
                          get(name=excel_name).
                          sheet_set.
                          values("name").
                          distinct())

            return JsonResponse({"sheet_data" : list(sheet_name)} , status=200)

        except KeyError :
            return HttpResponse(status=400)

        except TypeError:
            return HttpResponse(status=400)

    def delete(self, request , excel_name):

        if not Excel.objects.filter(name=excel_name).exists():
            return JsonResponse({"message", "DOESNOT_EXCEL"} , status=400)

        try:
            excel_name = Excel.objects.get(name = excel_name)
            print(excel_name)
            excel_name.delete()
            excel_name.save()

        except ValueError:
            return JsonResponse({"message" , "INVALID_VALUE"} , status=400)

        except KeyError:
            return JsonResponse({"message","INVALID_KEY"},status=400)

        except Exception as e:
            return JsonResponse({"message",e},status=400)


class SheetDetailView(View):
    def get(self , request, excel_name , sheet_name):
        if not Excel.objects.filter(name=excel_name).exists():
            return JsonResponse({"message":"DOESNOT_EXCEL"} , status=400)

        if not Sheet.objects.filter(name = sheet_name).exists():
            return JsonResponse({"message":"DOESNOT_SHEET"} , status=400)

        try :
            excel_id = Excel.objects.get(name=excel_name).id
            sheet_data = (Sheet.
                          objects.
                          filter(excel_name_id=excel_id , name = sheet_name).
                          values("Plate_No",
                                 "Replicate_No",
                                 "Well_No",
                                 "Index_No",
                                 "KaiChem_ID",
                                 "Conc_nM",
                                 "Cell",
                                 "Time",
                                 "RNA_Ext_Date",
                                 "Lib_Prep_Date",
                                 "Seq_Req_Date",
                                 "NGS_Data_Date",
                                 ))

            cols = []
            cols_dict= []
            cols.append("id")
            [cols.append(sheet) for sheet in sheet_data[0]]
            [cols_dict.append({"name":cols[num],"key":num}) for num in range(0 , len(cols))]

            rows = []
            for num in range(0 , len(sheet_data)):
                row = []
                [row.append(sheet) for sheet in sheet_data[num].values()]
                rows.append(row)

            return JsonResponse({"sheet_table": {
                                        "cols": cols_dict,
                                        "rows": rows,
                                    }}, status=200)

        except KeyError:
            return HttpResponse(status=400)

        except TypeError:
            return HttpResponse(status=400)

        except Exception as e:
            return JsonResponse({"message":e},status=400)
