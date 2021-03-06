from django.urls import path
from .views      import (ExcelView ,
                         ExcelDetailView,
                         SheetDetailView,
                         StatisticsPage)

urlpatterns = [
    path("upload"                            , ExcelView.as_view()),
    path("statistics"                        , StatisticsPage.as_view()),
    path("<str:excel_name>"                  , ExcelDetailView.as_view()),
    path("<str:excel_name>/<str:sheet_name>" , SheetDetailView.as_view()),
]
