from django.db import models


# Create your models here.

class User(models.Model):
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=32,default=None)
    token = models.CharField(max_length=250, default='123')
    status = models.IntegerField(default=1, verbose_name='状态 0:关闭 1:正常 2:异常')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    u_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = 't_user'
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'
