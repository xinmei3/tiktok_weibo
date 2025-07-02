import pymysql


class DataBase:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',  # replace with your database password
        database='database_name',  # replace with your database name
        charset='utf8mb4',
    )

    cursor = connection.cursor()

    def __init__(self):
        self.cursor = DataBase.cursor
        self.connection = DataBase.connection

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def return_diction(self, results):
        if results is None:
            return None
        else:
            columns = [col[0] for col in self.cursor.description]
            results = dict(zip(columns, results))
            return results

    def search_tiktok(self):
        sql = "SELECT * FROM tiktok order by id desc limit 1"  # replace with your table name
        self.cursor.execute(sql)
        results = self.cursor.fetchone()  # get last row data
        results = self.return_diction(results)
        return results  # return last row data

    def search_weibo(self):
        sql = "SELECT * FROM weibo order by id desc limit 1"  # replace with your table name
        self.cursor.execute(sql)
        results = self.cursor.fetchone()  # get last row data

        return results  # return last row data
    
    def insert_tiktok(self, data):
        sql = "INSERT INTO tiktok (粉丝数, 关注数, 获赞数, 作品数, 喜欢作品数, 时间) VALUES " + "(%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, data)
        self.connection.commit()  # submit the transaction

    def insert_weibo(self, data):
        sql = "INSERT INTO weibo (总获赞数, 评论数, 获赞数, 粉丝数, 关注数, 微博数, 时间) VALUES " + "(%s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, data)
        self.connection.commit() # submit the transaction


if __name__ == "__main__":
        # 测试代码
    database = DataBase()  # 创建数据库连接实例

    last_row = database.search_tiktok()  # 获取最后一行数据
    print(last_row)
