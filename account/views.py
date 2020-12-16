import json
import jwt
import bcrypt

from django.views               import View
from django.http                import HttpResponse , JsonResponse
from kmap_info_back.my_settings import SECRET_KEY , ALGORITHM
from .models                    import Account


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:

            if Account.objects.filter(user_id = data['user_id']).exists():
                user = Account.objects.get(user_id = data['user_id'])

                if bcrypt.checkpw(data['password'].encode('utf-8'),
                                  user.password.encode('utf-8')):

                    return HttpResponse(status=200)

                return HttpResponse(status = 401)

            return HttpResponse(status = 400)

        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)

        except Account.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status = 400)



