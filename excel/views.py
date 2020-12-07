import datetime
import numpy as np
import operator

from math         import ceil
from pprint       import pprint as pp
from collections  import Counter , OrderedDict

from .models      import (Excel,
                          Sheet)

from django.views import View
from django.http  import HttpResponse, JsonResponse
from openpyxl     import load_workbook


class ExcelView(View):

    def post(self, request):
        data       = request.FILES.get('file',None)

        if data is None:
            return JsonResponse({"message": "DOES_NOT_FILE"}, status = 400)

        sheetList  = []
        excel_name = str(data)

        try:

            if not data.name.endswith(".xlsx"):
                return JsonResponse({"message": "NOT_EXCEL_FILE"} , status = 400)

            if Excel.objects.filter(name = excel_name).exists():
                return JsonResponse({"message": "EXISTS_EXCEL"} , status = 400)

            Excel(
                name = excel_name
            ).save() # 저장

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

            cols      = ["id"]
            cols_dict = []
            cols      = [sheet for sheet in sheet_data[0]]
            cols_dict = [{"name" :cols[num],"key":num} for num in range(0,len(cols))]

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


def get_week_of_month(year, month,day):
    dt           = datetime.date(int(year),int(month),int(day))

    first_day    = dt.replace(day=1)
    dom          = dt.day
    adjusted_dom = dom + (1 + first_day.weekday()) % 7

    return int(ceil(adjusted_dom/7.0))

class StatisticsPage(View):
    def get(self, request):

        try:
            # circle
            kaichem_exclude = Sheet.objects.exclude(KaiChem_ID__in=["DMSO1",
                                                                    "DMSO2",
                                                                    "Niclo1",
                                                                    "Niclo2"]).values("KaiChem_ID").distinct().count()
            circle_number   = kaichem_exclude * 100 // 1364

            # columns
            sheet = (Sheet.
                     objects.
                     exclude(KaiChem_ID__in=["DMSO1","DMSO2" ,"Niclo1","Niclo2"]))
            data_list = ['20201019','20201019','20201019',
'20210319', '20210319','20210319','20210319','20210319','20210319','20210319','20210319','20210319','20210319','20210319','20210319','20210319','20210319','20210319','20210319','20201119','20201119','20201119','20201119','20201119','20201119','20201119','20201119','20201119','20201119','20201119','20201119','20201119','20201119',
'20201019','20201019','20201019','20201019','20201019','20201019','20201019','20201019','20201019','20201019', '20201019','20201019','20201019','20201019','20201019','20201019','20201019','20201019','20201019','20201019',
'20210223','20210223','20210223','20210223','20210223','20210223','20210223','20210223','20210223','20210223',
'20201019','20201019','20201019','20201019','20201019','20201019','20201019','20201019','20201019','20201019',
'20201019','20201019','20201019','20201019','20201019','20201019','20201019','20201019','20201019','20201019',
'20200819','20200819','20200819','20200819','20200819','20200819','20200819','20200819','20200819','20200819',
'20201220','20201220','20201220','20201220','20201220','20201220','20201220','20201220','20201220','20201220',
'20201120','20201120','20201120','20201120','20201120','20201120','20201120','20201120','20201120','20201120',
'20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020',
'20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020',
'20210120','20210120','20210120','20210120','20210120','20210120','20210120','20210120','20210120','20210120',
'20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020',
'20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020',
'20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020','20201020',
'20201020','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021',
'20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021',
'20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021',
'20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021',
'20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021',
'20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021','20201021']


#            data_list = [s.Library_Prep_date for s in sheet]
            new_data_list       = []
            new_data_json       = dict()

            for data in data_list:
                # formatting
                year  = data[0:4]
                month = data[4:6]
                day   = data[6:8]

                result    = get_week_of_month(year, month, day)
                temp_data = [year, month, result]
                new_data_list.append(temp_data)

            for new_data in new_data_list:
                if str(new_data[0]) not in new_data_json:
                    new_data_json[str(new_data[0])] = dict()
                if str(new_data[1]) not in new_data_json[str(new_data[0])]:
                    new_data_json[str(new_data[0])][str(new_data[1])] = [0]*6
                new_data_json[str(new_data[0])][str(new_data[1])][new_data[2]-1] += 1

            ordered_d1     = dict(**dict(OrderedDict(sorted(new_data_json.items()))))
            columns_array  = sorted(new_data_json.items() , reverse=True)
            columns_labels = []
            columns_data   = []

            for year in ordered_d1:
                for month in OrderedDict(sorted(new_data_json[year].items() , key=lambda t :t[0])):
                    for week in range(0 , len(new_data_json[year][month])):
                        if new_data_json[year][month][week] !=0:
                            columns_data.append(new_data_json[year][month][week])
                            columns_labels.append(f"{year}년{month} {week+1}주")

            while True:

                if len(columns_data) ==8:
                    break
                elif len(columns_data) < 8:
                    columns_labels.insert(0,"")
                    columns_data.insert(0,0)
                elif len(columns_data) > 8:
                    columns_labels = columns_labels[:8]
                    columns_data   = columns_data[:8]

            # svg
            svg_year_month_labels = [
            "2020101","2020102","2020103","2020104","2020105",
            "2020111","2020112","2020113","2020114","2020115",
            "2020121","2020122","2020123","2020124","2020125",
            "2021011","2021012","2021013","2021014","2021015",
            "2021021","2021022","2021023","2021024",
            "2021031","2021032","2021033","2021034","2021035",
            "2021041","2021042","2021043","2021044","2021045"]


            labels_list = ["10", "11" , "12", "1" , "2", "3", "4"]


            svg_weeks_list      = [i for i in range(1 , len(svg_year_month_labels)+1)]
            svg_data            = [0 for i in range(1 , len(svg_year_month_labels)+1)]
            svg_year_month_list = []

            for year in sorted([int(year) for year in new_data_json]):
                for svg in new_data_json:
                    if str(year) == svg:
                        for month in OrderedDict(sorted(new_data_json[svg].items() , key=lambda t :t[0])):
                            svg_year_month_list.append(f"{year}{month}")

            print(svg_year_month_list) # ['201910', '201911', '202008', '202010', '202011', '202012']

            return JsonResponse({
                "kaichem_number"      : kaichem_exclude,
                "circle_number"       : circle_number,
                "columns_data"        : columns_data,
                "columns_labels"      : columns_labels,
                "svg_data"            : svg_data,
                "svg_weeks_list"      : svg_weeks_list,
                "svg_year_month_list" : labels_list,
            }, status=200)

        except KeyError:
            return HttpResponse(status=400)

        except Exception as e:
            return JsonResponse({"message": e}, status=400)
