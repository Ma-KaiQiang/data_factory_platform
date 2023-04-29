from django.db import models


# Create your models here.
class Authorization(models.Model):
    sessionId = models.CharField(max_length=100)
    csrfToken = models.CharField(max_length=100)

    class Meta:
        db_table = "t_auth"


class DataFactoryIntranetConfig(models.Model):
    name = models.CharField(max_length=125, unique=True,default=None)
    host = models.GenericIPAddressField(unique=True,default=None)
    port = models.CharField(max_length=10, default=3306)
    user = models.CharField(max_length=125,default=None)
    password = models.CharField(max_length=125,default=None)
    remark = models.CharField(max_length=1000, null=True, default=None)
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "t_intranet_config"
