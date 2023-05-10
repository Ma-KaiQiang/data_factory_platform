import logging

from django.shortcuts import render, redirect
from data_sync.business.online_data_sync import OnlineDataSync
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from data_sync.models import DataFactoryIntranetConfig
from data_sync.util.online_auth import headers
from django.views.decorators.cache import cache_page
from data_sync.util.mysql_handle import PyMysqlBase

# Create your views here.
logger = logging.getLogger("django")


def index(request):
    return render(request, "index.html", {})


def get_header(request):
    return headers()


@csrf_exempt
def online_data_sync(request):
    if request.method == "POST":
        d = {
            "host": "192.168.2.43",
            "port": 3306,
            "database": "mabang",
            "table": "DB_Shop",
            "user": "mabang",
            "password": "mabang123"
        }
        online = OnlineDataSync()
        condition = request.body
        online_data = online.query(json.loads(condition))
        package = online.data_assemble(online_data)
        id = online.intranet_data_storage(package, condition=d)
        return JsonResponse({"id": id})
    if request.method == "GET":
        return render(request, "data_sync.html")


@csrf_exempt
def get_intranet_db(request):
    if request.method == 'GET':
        instance_name = request.GET.get("instance", None)
        db_name = request.GET.get("database", None)
        if instance_name == 'undefined':
            fields = ["id", "name", "host", "port", "user", "password", "remark"]
            data_l = list(DataFactoryIntranetConfig.objects.values_list(*fields))
            data = [dict(zip(fields, l)) for l in data_l]
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
            with PyMysqlBase(host=host, usr=user, pwd=password, port=int(port),database=db_name) as p:
                data = p.get_tables()
                data_ = list(map(lambda x: x[0], data))
            return JsonResponse({"success": True, "error": None, "data": data_})


def get_instance(request):
    if request.method == "GET":
        online = OnlineDataSync()
        data_ = online.query_instance()
        return JsonResponse({"success": True, "error": None, "data": data_})


def get_database(request):
    if request.method == "GET":
        online = OnlineDataSync()
        instance_name = request.GET.get("instance")
        data_ = online.query_database(instance_name=instance_name)
        return JsonResponse({"success": True, "error": None, "data": data_})


def get_table(request):
    if request.method == "GET":
        online = OnlineDataSync()
        instance_name = request.GET.get("instance")
        db_name = request.GET.get("database")
        data_ = online.query_table(instance_name=instance_name, db_name=db_name)
        return JsonResponse({"success": True, "error": None, "data": data_})


@csrf_exempt
def query(request):
    if request.method == "POST":
        on = OnlineDataSync()
        pat = json.loads(request.body.decode(encoding='utf8'))
        print(pat)
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
        if data.get('status') == 1:
            return JsonResponse(data)
        # query_data = on.data_assemble(data)
        return JsonResponse(data)


# 内网数据库配置
def get_intranet_config(request):
    if request.method == "GET":
        fields = ["id", "name", "host", "port", "user", "password", "remark"]
        data_l = list(DataFactoryIntranetConfig.objects.values_list(*fields))
        data = [dict(zip(fields, l)) for l in data_l]
        return render(request, "intranet_data_config.html", {"data": data})


@csrf_exempt
def add_intranet_config(request):
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
    if request.method == "POST":
        data = json.loads(request.body.decode(encoding="utf8"))
        DataFactoryIntranetConfig.objects.filter(id=data.get("id")).delete()
        return JsonResponse({"code": 0, "msg": "删除成功", "data": []})
