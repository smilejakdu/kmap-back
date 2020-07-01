from django.urls import path
from .views   import CompoundView

urlpatterns = [
    path("<int:chem_index>" , CompoundView.as_view()),
]
