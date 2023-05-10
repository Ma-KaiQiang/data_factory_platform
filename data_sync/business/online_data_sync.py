import json

import requests
from jsonpath import jsonpath
from data_sync.util.mysql_handle import PyMysqlBase
from data_sync.util.redis_handle import RedisHandle


def headers():
    client = RedisHandle().client
    header = client.hget('authorization', 'headers')
    return json.loads(header)


class OnlineDataSync():
    @staticmethod
    def query_instance():
        res = requests.get(url='https://wos.mabangerp.com/group/user_all_instances/?tag_codes[]=can_read',
                           headers=headers())
        mysql_l = jsonpath(res.json(), '$..data[?(@.db_type=="mysql")].instance_name')
        return mysql_l

    @staticmethod
    def query_database(instance_name):
        res = requests.get(
            f'https://wos.mabangerp.com/instance/instance_resource/?instance_name={instance_name}&resource_type=database',
            headers=headers())
        databases = jsonpath(res.json(), '$..data')[0]

        return databases

    @staticmethod
    def query_table(instance_name, db_name):
        res = requests.get(
            f'https://wos.mabangerp.com/instance/instance_resource/?instance_name={instance_name}&db_name={db_name}&resource_type=table',
            headers=headers())
        databases = jsonpath(res.json(), '$..data')[0]
        return databases

    @staticmethod
    def query(condition: dict) -> dict | bool:
        '''
        线上数据库数据查询业务
        :param condition: 查询条件
        :return: 查询结果
        '''
        data = {
            'instance_name': condition.get('instance_name'),
            'db_name': condition.get('db_name'),
            'tb_name': condition.get('tb_name'),
            'sql_content': condition.get('sql_content'),
            'limit_num': condition.get('limit_num'),
        }
        res = requests.post(url='https://wos.mabangerp.com/query/', data=data, headers=headers())
        if res.status_code == 200:
            res_data = res.json()
            data = res_data.get('data')
            if data:
                total = len(data.get('rows'))
                res_data['data']['total'] = total
                return res_data
            else:
                return False
        else:
            return False

    @staticmethod
    def data_assemble(data: dict) -> dict:
        '''
        查询结果数据拼装
        :param data: 接口返回数据
        :return: 返回list，迭代字典，列名与值的键值对.
        '''
        column_list = jsonpath(data, '$..column_list')[0]
        # column_list.pop(0)
        rows = jsonpath(data, '$..rows')[0]
        # r = [r.pop(0) for r in rows]
        package = {'column_list': column_list, 'rows': rows}
        return package



    def main(self):
        # 订单
        data = self.query({"instance": 'public-order-fahuo', "database": "mabang_order", "table": "Db_OrderType22",
                           "content": "select * from mabang_order.Db_OrderType22 where orderId in (41706860,41695842,41706858,41706859,41708314)"})
        # data = self.query({"instance": 'public-order-fahuo', "database": "mabang_order", "table": "Db_OrderType5",
        #                    "content": "select * from mabang_order.Db_OrderType5 where orderId in (21488888,21474489,21477465,21492521)"})
        ctx = self.data_assemble(data)
        print(ctx)
        condition = {"host": "192.168.2.43", "port": 3306, "user": "mabang", "password": "mabang123",
                     "database": "mabang_order", "table": 'Db_OrderType22'}
        id = self.intranet_data_storage(data=ctx, condition=condition)
        return id


class IntranetDataBase():

    def get_instance(self):
            pass
    @staticmethod
    def intranet_data_storage(data: dict, condition: dict):
        '''
        将线上查询到得数据存储到内网
        :param data: 线上数据
        :param condition: 链接数据库参数
        :return: 新增数据id list
        '''
        ids = []
        with PyMysqlBase(host=condition.get('host'), port=condition.get('port'), usr=condition.get('user'),
                         pwd=condition.get('password'), database=condition.get('database')) as p:
            for r in data.get('rows'):
                result = p.insert(table=condition.get('table'), fields=data.get('col'), values=r)
                if result:
                    ids.append(result)
        return ids
if __name__ == '__main__':
    on = OnlineDataSync()
    id = on.main()
    print(id)
