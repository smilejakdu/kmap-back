from django.urls import path
from .views      import (CompoundView ,
                         SearchView ,
                         CompoundNameView)

urlpatterns = [
    path("search"            , SearchView.as_view()),
    path("search/<str:name>" , CompoundNameView.as_view()),
    path("<int:chem_index>"  , CompoundView.as_view()),
]
