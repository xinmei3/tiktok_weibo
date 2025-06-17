import pymysql


class DataBase:        
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',  # 替换为你的数据库密码
        database='tiktok',  # 替换为你的数据库名称
        charset='utf8mb4',
    )
    cursor = connection.cursor()
    def __init__(self):
        self.cursor = DataBase.cursor
        self.connection = DataBase.connection

    def __del__(self):
        self.cursor.close()
        self.connection.close()


    def search_tiktok(self):
        sql = "SELECT * FROM tiktok order by id desc limit 1"  # 替换为你的表名
        self.cursor.execute(sql)
        results = self.cursor.fetchone()  # 获取最后一行数据
        return results  # 返回最后一行数据

    def search_weibo(self):
        sql = "SELECT * FROM weibo order by id desc limit 1"  # 替换为你的表名
        self.cursor.execute(sql)
        results = self.cursor.fetchone()  # 获取最后一行数据

        return results  # 返回最后一行数据
    
    def insert_tiktok(self, data):
        sql = "INSERT INTO tiktok (粉丝数, 关注数, 获赞数, 作品数, 喜欢作品数, 时间) VALUES " + "(%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, data)
        self.connection.commit()  # 提交事务

    def insert_weibo(self, data):
        sql = "INSERT INTO weibo (总获赞数, 评论数, 获赞数, 粉丝数, 关注数, 微博数, 时间) VALUES " + "(%s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, data)
        self.connection.commit() # 提交事务


if __name__ == "__main__":
        # 测试代码
    database = DataBase()  # 创建数据库连接实例

    last_row = database.search_tiktok()  # 获取最后一行数据
    new_tuple = last_row[1:-1]
    print(last_row)
