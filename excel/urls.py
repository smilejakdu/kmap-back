from django.urls import path
from .views      import (ExcelView ,
                         ExcelDetailView)
urlpatterns = [
    path("" , ExcelView , name="excel"),
]
