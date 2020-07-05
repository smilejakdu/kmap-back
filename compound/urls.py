from django.urls import path
from .views      import CompoundView , SearchView

urlpatterns = [
    path("search"           , SearchView.as_view()),
    path("<int:chem_index>" , CompoundView.as_view()),
]
