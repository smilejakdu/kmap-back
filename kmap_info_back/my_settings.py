
DATABASES = {
    'default': {
        'ENGINE'   : 'django.db.backends.mysql',
        'HOST'     : 'localhost',
        'NAME'     : 'snack_back',
        'USER'     : 'root',  # 유저 이름
        'PASSWORD' : '##tkakrnl12',  # 패스워드
        'PORT'     : '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_general_ci',
        }
    }
}

ALGORITHM = 'HS256'

SECRET_KEY = {
    'secret' :'snack!',
}
