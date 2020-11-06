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
                        print("name" , sheet)
                        print("Subset" , values[1])
                        print("Compound_concentration_nM" , values[2])
                        print("Replicate" , values[3])
                        print("KaiChem_ID" , values[4])
                        print("Compound Name" , values[5])
                        print("Compound treatment time" , values[6])
                        print("Cell line", values[7])
                        print("Plate ID", values[8])
                        print("Well",values[9])
                        print("Sample ID", values[10])
                        print("MGI Index No",values[11])
                        rna_date     = datetime.strptime(values[12],"%Y%m%d").timestamp()
                        livrary_date = datetime.strptime(values[13],"%Y%m%d").timestamp()
                        sample_date  = datetime.strptime(values[14],"%Y%m%d").timestamp()
                        print(ran_date)
                        print(livrary_date)
                        print(sample_date)
                        print("RNA quantity_ng",values[15])
                        print("DNA quantity_ng",values[16])

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
                            Library_Prep_Date         = values[13],
                            Sample_sending_date_LAS   = values[14],
                            RNA_quantity_ng           = values[15],
                            DNA_quantity_ng           = values[16],
                            excel_name_id             = Excel.objects.get(name=excel_name).id
                        )

            return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)

        except Exception as e:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)

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
            # DMSO1 , DMSO2 , Niclo1 , Niclo2 제외
            kaichem_number = Sheet.objects.values("KaiChem_ID").distinct().count()  # KaiChem_ID 의 수
            circle_number  = kaichem_number * 100 // 1364

            # columns
            sheet              = Sheet.objects.values("NGS_Data_Date")
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
