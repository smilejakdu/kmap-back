from django.db import models

class Account(models.Model):
    user_id   = models.CharField(max_length = 250, unique = True, verbose_name = 'user_id')
    password  = models.CharField(max_length = 500, null   = True)
    create_at = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = "accounts"

