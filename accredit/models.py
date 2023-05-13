from django.db import models


# Create your models here.

class User(models.Model):
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=32)
    token = models.CharField(max_length=255,default=None)
    status = models.IntegerField(default=1)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = 't_user'
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'
