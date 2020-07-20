from .models          import Excel, Sheet
from django.views     import View
from django.db.models import Count
from django.http      import HttpResponse, JsonResponse
from openpyxl         import load_workbook
from datetime         import datetime

import json
import xlrd
import dateutil.relativedelta


class ExcelView(View):
    def post(self, request):
        data       = request.FILES["file"]
        sheetList  = []
        excel_name = str(data)

        try:
            if not data.name.endswith(".xlsx"):
                return JsonResponse({"message": "NOT_EXCEL_FILE"}, status = 400)
            print("excel_name: ", excel_name);
            if Excel.objects.filter(name=excel_name).exists():
                return JsonResponse({"message": "EXISTS_EXCEL"}, status = 400)

            Excel(
                name=excel_name
            ).save()

            wb = load_workbook(data, data_only=True)
            [sheetList.append(i) for i in wb.sheetnames]

            for sheet in sheetList:
                sheet_row = wb[sheet]
                all_values = []

                for row in sheet_row.rows:
                    row_value = []
                    [row_value.append(cell.value) for cell in row]
                    all_values.append(row_value)

                for num, values in enumerate(all_values):
                    if not num == 0:
                        Sheet.objects.create(
                            name=sheet,
                            Subset=values[0],
                            Concentration_nM=values[1],
                            Replicate_No=values[2],
                            KaiChem_ID=values[3],
                            Cell=values[4],
                            Treat_Time=values[5],
                            Well_Location=values[6],
                            Index_No=values[7],
                            Seeding_Date=values[8],
                            RNA_Extraction_Date=values[9],
                            Library_Prep_Date=values[10],
                            Seq_Request_Date=values[11],
                            NGS_Data_Date=values[12],
                            excel_name_id=Excel.objects.get(name=excel_name).id
                        )

            return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)

    def get(self, request):
        try:
            query = request.GET.get('keyword', None)

            if query:
                excel_search = Excel.objects.filter(name__icontains=query).all()
                excel_data = [{
                    "id": excel.id,
                    "name": excel.name
                } for excel in excel_search]

                return JsonResponse({"data": excel_data}, status=200)

            excel_data = (Excel.
                          objects.
                          all().
                          values())
            excel_count = Excel.objects.count()

            return JsonResponse({"data": {
                "excel_data": list(excel_data),
                "excel_count": excel_count
            }}, status=200)

        except KeyError:
            return JsonResponse({"message", "INVALID_KEY"}, status=400)

        except TypeError:
            return JsonResponse({"message": "INVALID_TYPE"}, status=400)

        except Excel.DoesNotExist:
            return JsonResponse({"message": "DOESNOT_EXCEL"}, status=400)


class ExcelDetailView(View):
    def get(self, request, excel_name):

        if not Excel.objects.filter(name=excel_name).exists():
            return JsonResponse({"message": "DOESNOT_EXCEL"}, status=400)

        try:
            sheet_name = (Excel.
                          objects.
                          get(name=excel_name).
                          sheet_set.
                          values("name").
                          distinct())

            return JsonResponse({"sheet_data": list(sheet_name)}, status=200)

        except KeyError:
            return HttpResponse(status=400)

        except TypeError:
            return HttpResponse(status=400)

    def delete(self, request, excel_name):

        if not Excel.objects.filter(name=excel_name).exists():
            return JsonResponse({"message", "DOESNOT_EXCEL"}, status=400)

        try:
            excel_name = Excel.objects.get(name=excel_name)
            print(excel_name)
            excel_name.delete()

            return HttpResponse(status=200)

        except ValueError:
            return JsonResponse({"message", "INVALID_VALUE"}, status=400)

        except KeyError:
            return JsonResponse({"message", "INVALID_KEY"}, status=400)

        except Exception as e:
            return JsonResponse({"message", e}, status=400)


class SheetDetailView(View):
    def get(self, request, excel_name, sheet_name):
        if not Excel.objects.filter(name=excel_name).exists():
            return JsonResponse({"message": "DOESNOT_EXCEL"}, status=400)

        if not Sheet.objects.filter(name=sheet_name).exists():
            return JsonResponse({"message": "DOESNOT_SHEET"}, status=400)

        try:
            excel_id = Excel.objects.get(name=excel_name).id
            sheet_data = (Sheet.
                          objects.
                          filter(excel_name_id=excel_id, name=sheet_name).
                          values("Subset",
                                 "Concentration_nM",
                                 "Replicate_No",
                                 "KaiChem_ID",
                                 "Cell",
                                 "Treat_Time",
                                 "Well_Location",
                                 "Index_No",
                                 "Seeding_Date",
                                 "RNA_Extraction_Date",
                                 "Library_Prep_Date",
                                 "Seq_Request_Date",
                                 "NGS_Data_Date"
                                 ))

            cols = []
            cols_dict = []
            cols.append("id")
            [cols.append(sheet) for sheet in sheet_data[0]]
            [cols_dict.append({"name": cols[num], "key": num}) for num in range(0, len(cols))]

            rows = []
            for num in range(0, len(sheet_data)):
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
            return JsonResponse({"message": e}, status=400)


class StatisticsPage(View):
    def get(self, request):

        try:
            # circle info
            kaichem_number = Sheet.objects.values("KaiChem_ID").distinct().count()  # KaiChem_ID 의 수
            circle_number = kaichem_number * 100 // 1366

            # profiles per month
            now                = datetime.now()
            sheet              = Sheet.objects.values("NGS_Data_Date")
            month_diction      = {}

            for s in sheet:
                month_diction[str(s["NGS_Data_Date"])[:6]] = 0

            for s in sheet:
                date = str(s["NGS_Data_Date"])[:6] # 202007
                if date in month_diction:
                    month_diction[date] = month_diction[date] + 1

            print(month_diction) # {'202005': 8, '202004': 3, '202006': 5}

            # Total KMAP-2K Profile Numbers
            columns_list = []
            [columns_list.append({"name": month, "value": month_diction[month]}) for month in month_diction]

            # svg_data
            num = 0
            svg_data_list = []

            while True :
                print(str(now + dateutil.relativedelta.relativedelta(months = num)).split()[0].replace("-", "")[:6])
                date  = str(now + dateutil.relativedelta.relativedelta(months = num)).split()[0].replace("-", "")[:6] # 202006
                year  = date[:4] # 2020
                month = date[4:] # 06
                if int(month) < 10:
                    month = date[5:6]
                if Sheet.objects.filter(create_at__year__lte  = year ,
                                        create_at__month__lte = month).count() == 0: # 16
                    break
                svg_data_list.append({"name"  : f"{date}",
                                      "value" : Sheet.objects.filter(create_at__year__lte  = year ,
                                                                     create_at__month__lte = month).count()})
                num = num -1

            return JsonResponse({"data": {
                "kaichem_number" : kaichem_number,
                "circle_number"  : circle_number,
                "columns_list"   : columns_list,
                "svg_data_list"  : svg_data_list,
            }}, status=200)

        except KeyError:
            return HttpResponse(status=400)

        except Exception as e:
            return JsonResponse({"message": e}, status=400)
