import datetime
from .models          import (Excel,
                              Sheet)

from django.views     import View
from django.http      import HttpResponse, JsonResponse
from openpyxl         import load_workbook


class ExcelView(View):
    def post(self, request):
        data       = request.FILES["file"]
        sheetList  = []
        excel_name = str(data)
        print('excel_name :' , excel_name)

        try:
            if not data.name.endswith(".xlsx"):
                return JsonResponse({"message": "NOT_EXCEL_FILE"}, status = 400)

            if Excel.objects.filter(name = excel_name).exists():
                return JsonResponse({"message": "EXISTS_EXCEL"}, status = 400)

            Excel(
                name = excel_name
            ).save() # 저장 성공

            wb = load_workbook(data, data_only = True)
            [sheetList.append(i) for i in wb.sheetnames]

            for sheet in sheetList:
                sheet_row  = wb[sheet]
                all_values = []

                for row in sheet_row.rows:
                    row_value = [cell.value for cell in row]
                    all_values.append(row_value)

                for num, values in enumerate(all_values):
                    if not num == 0:

                        Sheet.objects.create(
                            name                      = sheet,
                            Subset                    = values[1],
                            Compound_concentration_nM = values[2],
                            Replicate                 = values[3],
                            KaiChem_ID                = values[4],
                            Compound_Name             = values[5],
                            Compound_treatment_time   = values[6],
                            Cell_line                 = values[7],
                            Plate_ID                  = values[8],
                            Well                      = values[9],
                            Sample_ID                 = values[10],
                            MGI_Index_No              = values[11],
                            RNA_Extraction_date       = values[12],
                            Library_Prep_date         = values[13],
                            Sample_sending_date_LAS   = values[14],
                            RNA_quantity_ng           = values[15],
                            DNA_quantity_ng           = values[16],
                            excel_name_id             = Excel.objects.get(name=excel_name).id
                        )

            return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)

        except Exception as e:
            return JsonResponse({"message": e}, status=400)

    def get(self, request):
        try:
            query = request.GET.get('keyword', None)

            if query:
                excel_search = Excel.objects.filter(name__icontains = query).all()
                excel_data   = [{
                    "id"   : excel.id,
                    "name" : excel.name
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
            excel_name = Excel.objects.get(name = excel_name)
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
            excel_id   = Excel.objects.get(name=excel_name).id
            sheet_data = (Sheet.
                          objects.
                          filter(excel_name_id=excel_id,
                                 name=sheet_name).
                                  values(
                                      "Subset", 
                                      "Compound_concentration_nM",
                                      "Replicate",
                                      "KaiChem_ID",
                                      "Compound_Name",
                                      "Compound_treatment_time",
                                      "Cell_line",
                                      "Plate_ID",
                                      "Well",
                                      "Sample_ID",
                                      "MGI_Index_No",
                                      "RNA_Extraction_date",
                                      "Library_Prep_date",
                                      "Sample_sending_date_LAS",
                                      "RNA_quantity_ng",
                                      "DNA_quantity_ng"))

            cols      = []
            cols_dict = []
            cols.append("id")

            [cols.append(sheet) for sheet in sheet_data[0]]
            [cols_dict.append({"name": cols[num], "key": num}) for num in range(0, len(cols))]

            rows = []
            for num in range(0, len(sheet_data)):
                row = []
                [row.append(sheet) for sheet in sheet_data[num].values()]
                rows.append(row)

            return JsonResponse({"sheet_table" : {
                "cols" : cols_dict,
                "rows" : rows,
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
            kaichem_exclude = Sheet.objects.exclude(KaiChem_ID__in=["DMSO1","DMSO2" ,"Niclo1","Niclo2"]).distinct().count()
            circle_number   = kaichem_exclude * 100 // 1364

            # columns
            sheet              = Sheet.objects.values("Library_Prep_date")
            month_diction      = {}

            for sheet_info in sheet:
                month_diction[str(sheet_info["NGS_Data_Date"])[:6]] = 0

            for sheet_info in sheet:
                year_month = str(sheet_info["NGS_Data_Date"])[:6] # 202007
                if year_month in month_diction:
                    month_diction[year_month] = month_diction[year_month] + 1

            columns_list = []
            [columns_list.append({"name" : str(month)[4:6],
                                  "value": month_diction[month]}) for month in sorted(month_diction.keys())]

            # svg
            svg_data_list = []
            svg_date      = []

            for s in sorted(month_diction.keys()):
                svg_date.append(s)

            for s in svg_date:
                svg_num = 0

                for k , v in month_diction.items():
                    if int(s) >= int(k):
                        svg_num = svg_num + int(v)

                svg_data_list.append({
                    "name"  : str(s)[4:6],
                    "value" : svg_num
                })

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
