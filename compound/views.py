from django.views import View
from django.http import JsonResponse
from .models import Compound


class CompoundView(View):
    def get(self, request, kaipharm_chem_id):

        # 값이 존재하는지 우선적으로 체크를 해준다
        if not Compound.objects.filter(id=kaipharm_chem_id).exists():
            return JsonResponse({"message": "DOES_NOT_COMPOUND"}, status=400)

        try:
            compound_info = (Compound.
                             objects.
                             filter(id=kaipharm_chem_id).
                             values())

            return JsonResponse({"data": list(compound_info)}, status=200)

        except TypeError:
            return JsonResponse({"message": "INVALID_TYPE"}, status=400)

        except Compound.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_COMPOUND"}, status=400)

        except Exception as e:
            return JsonResponse({"message": e}, status=400)


class SearchView(View):
    def get(self, request):

        # 검색값을 받는다
        search = request.GET.get("query", None)
        try:
            if len(search) > 0:
                compound_data = (Compound.
                                 objects.
                                 filter(compound__icontains=search).
                                 values())

                return JsonResponse({"data": list(compound_data)}, status=200)

        except TypeError:
            return JsonResponse({"message": "INVALID_TYPE"}, status=400)

        except Exception as e:
            return JsonResponse({"message": e}, status=400)


class CompoundNameView(View):
    def get(self, request, name):

        # 검색 결과값을 받는다

        try:
            compound = (Compound.
                        objects.
                        filter(compound=name).
                        values())

            return JsonResponse({"data": list(compound)}, status=200)

        except Compound.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST"}, status=400)

        except Exception as e:
            return JsonResponse({"message": e}, status=400)
