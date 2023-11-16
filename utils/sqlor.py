"""
@File: sqlor.py
@Author: 秦宇
@Created: 2023/11/5 14:03
@Description: Created in 咸鱼-自动化-AutoXhs.
"""
from dbutils.pooled_db import PooledDB


class MySQL:
    def __init__(self):
        self.pool = None

    def setParam(self, config: dict):
        self.pool = PooledDB(**config)

    @staticmethod
    def connect(func):
        def inner(self, *args, **kwargs):
            conn = self.pool.connection()
            cursor = conn.cursor()
            result = func(self, *args, **kwargs, conn=conn, cursor=cursor)
            cursor.close()
            conn.close()
            return result

        return inner

    @connect
    def create(self, table_name: str, columns: list | tuple, conn=None, cursor=None):
        try:
            if table_name.__contains__(' '):
                return []
            sql = f'CREATE TABLE IF NOT EXISTS {table_name} ('
            sql += ', '.join(columns)
            sql += ')'
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f" * Failed to create table {table_name}. Error: {e}")

    @connect
    def show(self, sql: str = None, conn=None, cursor=None):
        try:
            sql = sql or 'SHOW TABLES'
            cursor.execute(sql)
            tables = cursor.fetchall()
            for table in tables:
                print(f"\t{table[0]}")
        except Exception as e:
            print(f" * Failed to fetch tables. Error: {e}")

    @connect
    def insert(self, table: str, data: dict, conn=None, cursor=None):
        try:
            if table.__contains__(' '):
                return []
            keys = ','.join(data.keys())
            values = ','.join(['%s'] * len(data))
            insert_values = []
            for value in data.values():
                if isinstance(value, str) and value == 'false':
                    value = 0
                elif isinstance(value, str) and value == 'true':
                    value = 1
                insert_values.append(value)
            sql = f'INSERT INTO {table} ({keys}) VALUES ({values})'
            cursor.execute(sql, tuple(insert_values))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f' * Insert failed. Error: {e}')

    @connect
    def delete(self, table: str, condition: str, conn=None, cursor=None):
        try:
            if table.__contains__(' '):
                return []
            sql = f'DELETE FROM {table} WHERE {condition}'
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f' * Delete failed. Error: {e}')

    @connect
    def update(self, table: str, data: dict, condition: str, conn=None, cursor=None):
        try:
            if table.__contains__(' '):
                return []
            update_data = ','.join([f'{key}=%s' for key in data.keys()])
            update_values = []
            for value in data.values():
                if isinstance(value, str) and value == 'false':
                    value = 0
                elif isinstance(value, str) and value == 'true':
                    value = 1
                update_values.append(value)
            sql = f'UPDATE {table} SET {update_data} WHERE {condition}'
            cursor.execute(sql, tuple(update_values))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f' * Update failed. Error: {e}')

    @connect
    def select(self, table: str, fields: list = None, condition: str = '', count: int = 0, conn=None, cursor=None):
        if fields is None:
            fields = []
        try:
            if table.__contains__(' '):
                return []
            if not fields:
                sql = f'SELECT * FROM {table}'
            else:
                select_fields = ','.join(fields)
                sql = f'SELECT {select_fields} FROM {table}'
            if condition:
                sql += f' WHERE {condition}'
            cursor.execute(sql)
            if count <= 0:
                result = cursor.fetchall()
            elif count == 1:
                result = cursor.fetchone()
            else:
                result = cursor.fetchmany(count)
            return result
        except Exception as e:
            print(f' * Select failed. Error: {e}')


sql = MySQL()
