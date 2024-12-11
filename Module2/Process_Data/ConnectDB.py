import psycopg2

class ConnectDB:
    # 创建数据库连接
    def createConnect(self):
        # 连接数据库
        self.connect = psycopg2.connect(
            database = "Course:Big_Data",
            user = "postgres",
            password = "123456",
            host = "localhost",
            port = "5432"
        )
        self.cursor = self.connect.cursor()

    # 关闭连接
    def closeConnect(self):
        self.cursor.close()
        self.connect.close()

    # 查询全部数据
    def selectAll(self):
        selectSQL = "SELECT * FROM music_info_json_table;"
        self.cursor.execute(selectSQL)
        list = self.cursor.fetchall()
        result = []
        for item in list:
            result.append(item[1])
        return result

# ConnectDB = ConnectDB()
# ConnectDB.createConnect()
# print(ConnectDB.selectAll())
# ConnectDB.closeConnect()
