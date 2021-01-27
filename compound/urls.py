from django.urls import path
from .views      import (CompoundView ,
                         SearchView ,
                         CompoundNameView)

urlpatterns = [
    path("search"                 , SearchView.as_view()), # 검색 input
    path("search/<str:name>"      , CompoundNameView.as_view()), # 검색 result
    path("<int:kaipharm_chem_id>" , CompoundView.as_view()), # up down button
]
