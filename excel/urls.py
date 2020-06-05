from django.urls import path
from .views      import (ExcelView ,
                         ExcelDetailView)

urlpatterns = [
    path("upload" , ExcelView.as_view()),
    path("<str:excel_name>" , ExcelDetailView.as_view()),
]
