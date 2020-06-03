import json
from .models         import GeneData
from account.utils   import login_check
from django.views    import View
from django.http     import HttpResponse, JsonResponse

import csv
import pandas as pd
import re

class ExcelView(View):
    @login_check
    def post(self , request):
        data = json.loads(request.data)

        xlsx = pd.read_excel("venture_company2.xlsx")
        xlsx.to_csv("./venture_company2.csv")
        try:
            print("")

        except:
            return

    @login_check
    def get(self , request):
        return


class ExcelDetailView(View):
   def post(self , request):
       return

   def delete(self , request):
       return
