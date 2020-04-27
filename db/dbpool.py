# python 3.7.4
# coding = utf-8
# filename dbpool.py
# author 463714869@qq.com/www.cdzcit.com,
#        create by VIM at 2020/1/3

import configparser
import os
import pymysql
from DBUtils.PooledDB import PooledDB
from pymysql.cursors import DictCursor


class Config(object):
    """
    [MysqlDatabaseInfo]
    db_host = 192.168.1.101
    db_port = 3306
    db_user = root
    db_password = python123
    db_name = 123
    """

    def __init__(self, config_filename='dbconfig.cnf'):
        file_path = os.path.join(os.path.dirname(__file__), config_filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path)

    def get_sections(self):
        """
        :return:
        """
        return self.cf.sections()

    def get_options(self, section):
        """
        :param section: get_sections
        :return:
        """
        return self.cf.options(section)

    def get_content(self, section):
        """
        :param section: get_sections
        :return:
        """
        result = {}
        for option in self.get_options(section):
            value = self.cf.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result


class BasePymysqlPool(object):
    def __init__(self, db_host, db_port, db_user, db_password, db_name):
        """
        :param db_host: 数据库地址
        :param db_port: 数据库端口
        :param db_user: 数据库用户
        :param db_password: 数据库用户密码
        :param db_name: 数据库名
        """
        self.db_host = db_host
        self.db_port = int(db_port)
        self.db_user = db_user
        self.db_password = str(db_password)
        self.db_name = db_name


class MyPymysqlPool(BasePymysqlPool):
    """
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = Mysql.getConn()
    释放连接对象;conn.close()或del conn
    """
    # 连接池对象
    __pool = None

    def __init__(self, logger, conf_name='MysqlDatabaseInfo'):
        """
        :param logger: 日志对象
        :param conf_name: 配置文件中的配置章节名称
        """
        self.conf = Config().get_content(conf_name)
        super(MyPymysqlPool, self).__init__(**self.conf)
        self._pool = PooledDB(creator=pymysql,
                              mincached=1,
                              maxcached=64,
                              host=self.db_host,
                              port=self.db_port,
                              user=self.db_user,
                              passwd=self.db_password,
                              db=self.db_name,
                              use_unicode=True,
                              charset='utf8',
                              cursorclass=DictCursor)
        self._logger = logger

    def getAll(self, sql, param=None):
        """
        :param sql:查询SQL，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        :param param: 可选参数，条件列表值（元组/列表）
        :return: result list(字典对象)/boolean查询到的结果集
        """
        result = None
        _conn = self._pool.connection()
        _cursor = _conn.cursor()
        try:
            if param is None:
                count = _cursor.execute(sql)
            else:
                count = _cursor.executemany(sql, param)
        except Exception as e:
            if self._logger is not None:
                self._logger.error('SQL语句执行错误: %s - %s' % (sql, e))
            else:
                print('SQL语句执行错误: %s - %s' % (sql, e))
            _conn.rollback()
        else:
            if self._logger is not None:
                self._logger.debug('%s : get %d datas' % (__name__, count))
            else:
                print('%s : get %d datas' % (__name__, count))
            if count > 0:
                result = _cursor.fetchall()
            _conn.commit()
        finally:
            _cursor.close()
            _conn.close()
            return result

    def getOne(self, sql, param=None):
        """
        :param sql: 查询SQL，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        :param param: 可选参数，条件列表值（元组/列表）
        :return: result list/boolean查询到的结果集
        """
        result = None
        _conn = self._pool.connection()
        _cursor = _conn.cursor()
        try:
            if param is None:
                count = _cursor.execute(sql)
            else:
                count = _cursor.executemany(sql, param)
        except Exception as e:
            if self._logger is not None:
                self._logger.error('SQL语句执行错误: %s - %s' % (sql, e))
            else:
                print('SQL语句执行错误: %s - %s' % (sql, e))
            _conn.rollback()
        else:
            if self._logger is not None:
                self._logger.debug('%s : get %d datas' % (__name__, count))
            else:
                print('%s : get %d datas' % (__name__, count))
            if count > 0:
                result = _cursor.fetchone()
            _conn.commit()
        finally:
            _cursor.close()
            _conn.close()
            return result

    def getMany(self, sql, num, param=None):
        """
        :param sql: 查询SQL，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        :param num: 取得的结果条数
        :param param: 可选参数，条件列表值（元组/列表）
        :return: result list/boolean查询到的结果集
        """
        result = None
        _conn = self._pool.connection()
        _cursor = _conn.cursor()
        try:
            if param is None:
                count = _cursor.execute(sql)
            else:
                count = _cursor.executemany(sql, param)
        except Exception as e:
            if self._logger is not None:
                self._logger.error('SQL语句执行错误: %s - %s' % (sql, e))
            else:
                print('SQL语句执行错误: %s - %s' % (sql, e))
            _conn.rollback()
        else:
            if self._logger is not None:
                self._logger.debug('%s : get %d datas' % (__name__, count))
            else:
                print('%s : get %d datas' % (__name__, count))
            if count > 0:
                result = _cursor.fetchmany(num)
            _conn.commit()
        finally:
            _cursor.close()
            _conn.close()
            return result

    def insertMany(self, sql, values):
        """
        :param sql: 要插入的SQL格式
        :param values: 要插入的记录数据tuple(tuple)/list[list]
        :return: count受影响的行数
        """
        count = 0
        if not values:
            return count
        _conn = self._pool.connection()
        _cursor = _conn.cursor()
        try:
            count = _cursor.executemany(sql, values)
        except Exception as e:
            if self._logger is not None:
                self._logger.error('SQL语句执行错误: %s - %s' % (sql, e))
            else:
                print('SQL语句执行错误: %s - %s' % (sql, e))
            _conn.rollback()
        else:
            if self._logger is not None:
                self._logger.debug('%s : insert %d datas' % (__name__, count))
            _conn.commit()
        finally:
            _cursor.close()
            _conn.close()
            return count

    def __query(self, sql, param=None):
        """
        :param sql: 要查询的SQL语句
        :param param: SQL语句的参数
        :return: count受影响行数
        """
        count = 0
        _conn = self._pool.connection()
        _cursor = _conn.cursor()
        try:
            if param is None:
                count = _cursor.execute(sql)
            else:
                count = _cursor.executemany(sql, param)
        except Exception as e:
            if self._logger is not None:
                self._logger.error('SQL语句执行错误: %s - %s' % (sql, e))
            else:
                print('SQL语句执行错误: %s - %s' % (sql, e))
            _conn.rollback()
        else:
            if self._logger is not None:
                self._logger.debug('SQL语句执行成功: %s - %d' % (sql, count))
            else:
                print('SQL语句执行成功: %s - %d' % (sql, count))
            _conn.commit()
        finally:
            _cursor.close()
            _conn.close()
            return count

    def update(self, sql, param=None):
        """
        :param sql: SQL格式及条件，使用(%s,%s)
        :param param: 要更新的值 tuple/list
        :return: count 受影响的行数
        """
        return self.__query(sql, param)

    def insert(self, sql, param=None):
        """
        :param sql: SQL格式及条件，使用(%s,%s)
        :param param: 要更新的  值 tuple/list
        :return: count受影响的行数
        """
        return self.__query(sql, param)

    def delete(self, sql, param=None):
        """
        :param sql: SQL格式及条件，使用(%s,%s)
        :param param: 要删除的条件 值 tuple/list
        :return: count受影响的行数
        """
        return self.__query(sql, param)

    def dispose(self):
        """
        释放连接池资源
        """
        try:
            self._pool.close()
        except Exception as e:
            if self._logger is not None:
                self._logger.error('释放资源出错: %s' % e)
            else:
                print('释放资源出错: %s' % e)


# 测试
if __name__ == '__main__':
    mysql = MyPymysqlPool(None, 'MysqlDatabaseInfo')

    sqlAll = "select code,name from t_stocks;"
    result = mysql.getAll(sqlAll)
    print(result)

    result = mysql.getMany(sqlAll, 10)
    print(result)

    result = mysql.getOne(sqlAll)
    print(result)

    # 释放资源
    mysql.dispose()