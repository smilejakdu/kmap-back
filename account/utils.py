import jwt

from excel.models               import Account
from kmap_info_back.my_settings import ALGORITHM, SECRET_KEY
from django.http                import JsonResponse


def login_check(func):
    def wrapper(self, request, *args, **kwargs):

        try:
            auth_token   = request.headers.get('Authorization', None)
            payload      = jwt.decode(auth_token,
                                      SECRET_KEY['secret'],
                                      algorithms=ALGORITHM)

            account         = Account.objects.get(email=payload["user_id"])
            request.account = account

            return func(self, request, *args, **kwargs)

        except User.DoesNotExist:
            return HttpResponse(status=400)

        except KeyError:
            return HttpResponse(status=400)

        except jwt.DecodeError:
            return HttpResponse(status=400)

    return wrapper
