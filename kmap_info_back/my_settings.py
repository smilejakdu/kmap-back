DATABASES = {
    'default' : {
        'ENGINE'   : 'django.db.backends.mysql',
        'HOST'     : '203.255.181.89',
        'NAME'     : 'KMAP__INFO',
        'USER'     : 'kmapinfo',
        'PASSWORD' : 'kmapinfo@!',
        'PORT'     : '3307',
        'TEST'     :
            {
                'CHARSET'   : 'utfmb4',
                'COLLATION' : 'utf8mb4_general_ci',
            }
    }
}
SECRET_KEY = {
    'secret' :'62rn^x%z_&q=wpzyr$f_7l2h&_v1=(72nt$v)ih-*z2sf@peu$',
}
ALGORITHM = 'HS256'



