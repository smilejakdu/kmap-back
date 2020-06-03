from django.shortcuts import render
import json
import jwt
import re
import bcrypt
import requests

from django.views               import View
from django.http                import HttpResponse, JsonResponse
from django.core.exceptions     import ValidationError

from kmap_info_back.my_settings import SECRET_KEY,   ALGORITHM
from .utils                     import login_check
from .models                    import Account


class SignUpView(View):

    def post(self, request):
        data     = json.loads(request.body)
        try :
            if data["user_id"] == "kmap" and data["password"] == "kaipharm1113":
                Account(
                    user_id  = data["user_id"],
                    password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                ).save()
                return HttpResponse(status=200)
                 
        except ValidationError:
            return HttpResponse(status=400)

        except KeyError:
            return HttpResponse(status=400)


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:

            if Account.objects.filter(user_id=data['user_id']).exists():
                user = Account.objects.get(email=data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'),
                                  user.password.encode('utf-8')):

                    token = jwt.encode({'email': data['email']},
                                           SECRET_KEY['secret'],
                                           algorithm=ALGORITHM).decode()

                    return JsonResponse({'access': token}, status=200, content_type="application/json")

                return HttpResponse(status=401)

            return HttpResponse(status=400)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status=400)

        except Account.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=400)



