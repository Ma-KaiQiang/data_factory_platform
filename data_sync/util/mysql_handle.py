# -*- coding: utf-8 -*-
'''
@Time    : 2022/11/16 10:24
@Author  : MaKaiQiang
@File    : pymysql
'''
import logging

import pymysql

logger = logging.getLogger('console')


class PyMysqlBase:

    def __init__(self, host: str, port: int, usr: str, pwd: str, database: str):
        self.conn = pymysql.connect(host=host, port=port, user=usr, password=pwd
                                    , database=database)
        self.cursor = self.conn.cursor()

    def cmd(self, sql):
        self.cursor.execute(sql)

    def insert(self, table, fields, values):
        '''
        向表内插入数据
        :param table:数据库表
        :param fields: 字段list
        :param values: 值list
        :return: id
        '''
        try:
            sql = f'insert into {table} ({fields}) values {tuple(values)}'.replace('None', 'null')
            print(sql)
            self.cursor.execute(sql)
            id = self.conn.insert_id()
            self.conn.commit()
            return id
        except Exception as e:
            self.conn.rollback()
            logger.error(f'{table}表插入数据错误：{e}')
            return False

    def select(self, table, field, condition=False):
        '''
        查询表数据
        :param table: 表名称
        :param field: 表字段
        :param condition: 查询条件
        :return: 数据
        '''
        try:
            if condition:
                key = list(condition.keys())[0]
                value = list(condition.values())[0]
                text = f'select {field} from {table} where {key}="{value}"'
            else:
                text = f'select {field} from {table} where {field} is not null '
            self.cursor.execute(text)
            data = self.cursor.fetchall()
            data = list(map(lambda x: x[0], data))
            return data
        except Exception as e:
            logger.error(f'{table}表查询数据错误：{e}')
            return False

    def field_is_exists(self, table, field):
        try:
            content = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}' and column_name = '{field}';"
            self.cursor.execute(content)
            result = self.cursor.fetchall()
            if result:
                return True
            else:
                logger.info(f'{table}表中，不存在{field}字段，新增此列.')
                sql = f'alter table {table} add {field} varchar(255)'
                self.cursor.execute(sql)
                self.conn.commit()
                return True
        except Exception as e:
            logger.error(e)
            return False

    def select_dictionary(self, type):
        sql = f"select dicTypeCode from t_dictionary_info where dicTypeGroupCode='{type}' and dicTypeCode!='unknown' ;"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        data = list(map(lambda x: x[0], data))
        return data

    # def modify(self, table, fields, values):
    #     try:
    #         if self.field_is_exists(table, fields):
    #             sql = f'UPDATE {table} SET {fields} = (%s) WHERE id = (%s)'
    #             self.cursor.executemany(sql, tuple(values))
    #             self.conn.commit()
    #             print(Fore.GREEN + '-' * 81 + ' Storage ' + '-' * 81)
    #             for v in values:
    #                 print(Fore.YELLOW + f'* {v[0]} update to table "{table}" index = {v[1]} field = "{fields}"')
    #         else:
    #             raise
    #     except Exception as e:
    #         self.conn.rollback()
    #         logger.error(f'{table}表插入数据错误：{e}')

    def delete(self, table):
        try:
            text = f'delete from {table};'
            self.cursor.execute(text)
            self.conn.commit()
        except Exception as e:
            logger.debug(f'清空{table}表中数据出错:{e}')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    pass
