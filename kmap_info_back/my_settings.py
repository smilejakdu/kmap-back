DATABASES = {
    'default': {
        'ENGINE'   : 'django.db.backends.mysql',
        'HOST'     : '203.255.181.89',
        'NAME'     : 'KMAP__INFO',
        'USER'     : 'kmapinfo',
        'PASSWORD' : 'kmapinfo@!',
        'PORT'     : '3307',
        'OPTIONS'  : {'charset': 'utf8mb4'},
        'TEST'     :
            {
            'CHARSET'  : 'utf8mb4',
            'COLLATION': 'utf8mb4_general_ci',
            }
        }
    }

#DATABASES = {
#    'default': {
#        'ENGINE'   : 'django.db.backends.mysql',
#        'HOST'     : 'localhost',
#        'NAME'     : 'KMAP__INFO',
#        'USER'     : 'root',
#        'PASSWORD' : '##tkakrnl12',
#        'PORT'     : '3306',
#        'OPTIONS'  : {'charset': 'utf8mb4'},
#        'TEST'     :
#            {
#            'CHARSET'  : 'utf8mb4',
#            'COLLATION': 'utf8mb4_general_ci',
#            }
#        }
#    }
#

ALGORITHM = 'HS256'

SECRET_KEY = {
    'secret' :'62rn^x%z_&q=wpzyr$f_7l2h&_v1=(72nt$v)ih-*z2sf@peu$',
}
