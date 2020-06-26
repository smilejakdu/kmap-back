
DATABASES = {
    'default': {
        'ENGINE'   : 'django.db.backends.mysql',
        'HOST'     : '203.255.181.89',
        'NAME'     : 'KMAP__INFO',
        'USER'     : 'kmapinfo',  # 유저 이름
        'PASSWORD' : 'kmapinfo@!',  # 패스워드
        'PORT'     : '3307',
        'OPTIONS': {'charset': 'utf8mb4'},
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_general_ci',
        }
    }
}

ALGORITHM = 'HS256'

SECRET_KEY = {
    'secret' :'62rn^x%z_&q=wpzyr$f_7l2h&_v1=(72nt$v)ih-*z2sf@peu$',
}
