import logging

from django.shortcuts import render, redirect
from data_sync.business.online_data_sync import OnlineDataSync, IntranetDataBase
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from data_sync.models import DataFactoryIntranetConfig
from data_sync.util.online_auth import headers
from django.views.decorators.cache import cache_page
from data_sync.util.mysql_handle import PyMysqlBase

# Create your views here.
logger = logging.getLogger("django")


def get_header(request):
    return headers()


@csrf_exempt
def online_data_sync(request):
    '''
    将选中的外网数据同步至内网
    :param request:
    :return:
    '''
    if request.method == "POST":
        d = {
            "host": "192.168.2.43",
            "port": 3306,
            "database": "mabang",
            "table": "DB_Shop",
            "user": "mabang",
            "password": "mabang123"
        }
        intranet_data = IntranetDataBase()
        condition = json.loads(request.body)
        id = intranet_data.intranet_data_storage(data={}, condition=condition)
        return JsonResponse({"id": id})
    if request.method == "GET":
        return render(request, "data_sync.html")


@csrf_exempt
def get_intranet_db(request):
    '''
    获取内网数据库列表
    :param request:
    :return:
    '''
    if request.method == 'GET':
        instance_name = request.GET.get("instance", None)
        db_name = request.GET.get("database", None)
        if instance_name == 'undefined':
            fields = ["id", "name", "host", "port", "user", "password", "remark"]
            data = list(DataFactoryIntranetConfig.objects.values_list('name'))
            return JsonResponse({'success': True, 'data': data})
        elif instance_name != 'undefined' and db_name == 'undefined':
            instance = DataFactoryIntranetConfig.objects.get(name=instance_name)
            host = instance.host
            user = instance.user
            password = instance.password
            port = instance.port
            with PyMysqlBase(host=host, usr=user, pwd=password, port=int(port)) as p:
                data = p.get_database()
                data_ = list(map(lambda x: x[0], data))
            return JsonResponse({"success": True, "error": None, "data": data_})
        else:
            instance = DataFactoryIntranetConfig.objects.get(name=instance_name)
            host = instance.host
            user = instance.user
            password = instance.password
            port = instance.port
            with PyMysqlBase(host=host, usr=user, pwd=password, port=int(port), database=db_name) as p:
                data = p.get_tables()
                data_ = list(map(lambda x: x[0], data))
            return JsonResponse({"success": True, "error": None, "data": data_})


def get_online_db(request):
    '''
    获取线上数据库列表
    :param request:
    :return:
    '''
    if request.method == 'GET':
        instance_name = request.GET.get("instance", None)
        db_name = request.GET.get("database", None)
        online = OnlineDataSync()
        if instance_name == 'undefined':
            data_ = online.query_instance()
            return JsonResponse({"success": True, "error": None, "data": data_})
        elif instance_name != 'undefined' and db_name == 'undefined':
            data_ = online.query_database(instance_name=instance_name)
            return JsonResponse({"success": True, "error": None, "data": data_})
        else:
            data_ = online.query_table(instance_name=instance_name, db_name=db_name)
            return JsonResponse({"success": True, "error": None, "data": data_})


@csrf_exempt
def query(request):
    '''
    查询线上表数据
    :param request:
    :return:
    '''
    if request.method == "POST":
        on = OnlineDataSync()
        pat = json.loads(request.body.decode(encoding='utf8'))
        instance_name = pat.get("instance_name")
        db_name = pat.get("db_name")
        tb_name = pat.get("tb_name")
        sql_content = pat.get("sql_content")
        limit_num = pat.get("limit_num")
        data = on.query({
            "instance_name": instance_name,
            "db_name": db_name,
            "tb_name": tb_name,
            "sql_content": sql_content,
            "limit_num": limit_num
        })
        if data:
            return JsonResponse(data)
        else:

            return JsonResponse({"success": False, 'msg': 'sql拼写有误'})


# 内网数据库配置
def get_intranet_config(request):
    '''
    获取内网配置列表
    :param request:
    :return:
    '''
    if request.method == "GET":
        fields = ["id", "name", "host", "port", "user", "password", "remark"]
        data_l = list(DataFactoryIntranetConfig.objects.values_list(*fields))
        data = [dict(zip(fields, l)) for l in data_l]
        return render(request, "intranet_data_config.html", {"data": data})


@csrf_exempt
def add_intranet_config(request):
    '''
    添加内网配置
    :param request:
    :return:
    '''
    if request.method == "POST":
        name = request.POST.get("config-name")
        host = request.POST.get("config-host")
        port = request.POST.get("config-port")
        user = request.POST.get("config-user")
        password = request.POST.get("config-password")

        remark = request.POST.get("config-remark", "")
        obj = DataFactoryIntranetConfig.objects.create(name=name, host=host, user=user, password=password, port=port,
                                                       remark=remark)
        DataFactoryIntranetConfig.save(obj)

        return redirect(get_intranet_config)


@csrf_exempt
def update_intranet_config(request):
    '''
    更新内网配置
    :param request:
    :return:
    '''
    if request.method == "POST":
        name = request.POST.get("config-name")
        host = request.POST.get("config-host")
        port = request.POST.get("config-port")
        user = request.POST.get("config-user")
        password = request.POST.get("config-password")
        remark = request.POST.get("config-remark", "")
        DataFactoryIntranetConfig.objects.filter(name=name).update(name=name, host=host, user=user, password=password,
                                                                   port=port,
                                                                   remark=remark)
        return redirect(get_intranet_config)


@csrf_exempt
def delete_intranet_config(request):
    '''
    删除内网配置
    :param request:
    :return:
    '''
    if request.method == "POST":
        data = json.loads(request.body.decode(encoding="utf8"))
        DataFactoryIntranetConfig.objects.filter(id=data.get("id")).delete()
        return JsonResponse({"code": 0, "msg": "删除成功", "data": []})
