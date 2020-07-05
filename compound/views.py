from django.views import View
from django.http  import HttpResponse , JsonResponse
from .models      import Compound


class CompoundView(View):
    def get(self , request , chem_index):
        print(chem_index)
        if not chem_index:
            return JsonResponse({"message" : "DOES_NOT_CHEM_INDEX"} , status=400)

        try :
            compound_info = (Compound.
                             objects.
                             filter(kaipharm_chem_index = chem_index).
                             values("subset",
                                    "japan",
                                    "europe",
                                    "usa",
                                    "nci_cancer",
                                    "kaichem_id",
                                    "kaipharm_chem_index",
                                    "chem_series",
                                    "chem_series_cid",
                                    "compound",
                                    "cid",
                                    "inchikey",
                                    "pubchem_name",
                                    "ipk",
                                    "prestwick",
                                    "selleckchem",
                                    "known_target",
                                    "information"))

            return JsonResponse({"data" : list(compound_info)} , status=200)

        except Compound.DoesNotExist:
            return JsonResponse({"message" : "DOES_NOT_COMPOUND"} , status=400)

        except TypeError:
            return JsonResponse({"message" : "INVALID_TYPE"}, status=400)

        except Exception as e:
            return JsonResponse({"message" : e} , status=400)


class SearchView(View):
    def get(self, request):
        search = request.GET.get("query" ,None)

        try :
            if len(search) > 0:
                compound_data = (Compound.
                                 objects.
                                 filter(compound__icontains = search).
                                 values("subset",
                                        "japan",
                                        "europe",
                                        "usa",
                                        "nci_cancer",
                                        "kaichem_id",
                                        "kaipharm_chem_index",
                                        "chem_series",
                                        "chem_series_cid",
                                        "compound",
                                        "cid",
                                        "inchikey",
                                        "pubchem_name",
                                        "ipk",
                                        "prestwick",
                                        "selleckchem",
                                        "known_target",
                                        "information"))

                return JsonResponse({"data" : list(compound_data)},status = 200)

        except TypeError:
            return JsonResponse({"message" : "INVALID_TYPE"},status = 400)

        except Exception as e :
            return JsonResponse({"message" : e}, status = 400)


class CompoundNameView(View):
    def get(self , request , name):

        try:
            compound = (Compound.
                        objects.
                        filter(compound = name).
                        values("subset",
                               "japan",
                               "europe",
                               "usa",
                               "nci_cancer",
                               "kaichem_id",
                               "kaipharm_chem_index",
                               "chem_series",
                               "chem_series_cid",
                               "compound",
                               "cid",
                               "inchikey",
                               "pubchem_name",
                               "ipk",
                               "prestwick",
                               "selleckchem",
                               "known_target",
                               "information"))

            return JsonResponse({"data" : list(compound)} , status = 200)

        except Compound.DoesNotExist:
            return JsonResponse({"message" : "DOES_NOT_EXIST"}, status = 400)

        except Exception as e:
            return JsonResponse({"message" : e}, status = 400)

