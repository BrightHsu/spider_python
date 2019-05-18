
import pymysql


# 打开数据库连接 参数：主机地址 端口号（统一为3306） 用户名 密码 数据库名字
db = pymysql.Connect(host="localhost", port=3306, user="test", passwd="123456", db="stu", charset="utf8")
cursor = db.cursor()  # 添加数据库游标

sql = """create table test_db(
        id int not null,
        name varchar(20),
        age int
        )"""
cursor.execute(sql)     # 执行sql创建test_db表

name = ["张三", "李四", "王五", "科比", "迈克尔"]
age = [13, 23, 42, 47, 33]
for i in range(len(age)):
    sql1 = """insert into test_db(id,name,age)
            values('{}','{}','{}')""".format(i+1, name[i], age[i])

    cursor.execute(sql1)    # 添加test_db表数据
db.commit()  # 提交添加
db.close()
print(db)

# # 3.数据库更新操作
# db = pymysql.Connect(host="localhost", port=3306, user="test", passwd="123456", db="stu", charset="utf8")
# cursor = db.cursor()  # 创建一个游标对象 cursor()
#
# sql3 = """update student set age=age+10 where id=3"""
# cursor.execute(sql3)
# db.commit()
# db.close()

# 4.删除操作
# db = pymysql.Connect(host="localhost", port=3306, user="test", passwd="123456", db="stu", charset="utf8")
# cursor = db.cursor()  # 创建一个游标对象 cursor()
#
# sql3 = """delete from student where name="lisi" """
# cursor.execute(sql3)
#
# db.commit()
# db.close()

