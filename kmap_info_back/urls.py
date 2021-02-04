from django.urls import path , include

urlpatterns = [
    path("excel/"    , include("excel.urls")),
    path("account/"  , include("account.urls")),
    path("compound/" , include("compound.urls")),
]
