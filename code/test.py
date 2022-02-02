# new0 = input()
# val = list()
# val.append("abc")
# sql = "UPDATE login SET password = " + new0 + " WHERE id = \"%s\""
# print(sql)

import mysql.connector
from mysql.connector import Error

# # def checkTableExists(hd1, tablename):
# #     mycursor = hd1.cursor()
# #     mycursor.execute("""
# #         SELECT COUNT(*)
# #         FROM information_schema.tables
# #         WHERE table_name = '{0}'
# #         """.format(tablename.replace('\'', '\'\'')))
# #     if mycursor.fetchone()[0] == 1:
# #         return True
# #     return False


def func(name):
    print('Hello ' + name)

hdl = None
try:
    hdl = mysql.connector.connect(
        host="mysqlServer", port="3306", user="root", passwd="password", database="project")
    mycursor = hdl.cursor()
    if hdl.is_connected():
        print('Connected to MySQL database')
except:
    print(Error)


# id = input('Enter doctor ID: ')
# mycursor.execute("SELECT id FROM doctor")
# idList = mycursor.fetchall()
# if (id,) in idList:
#     print('found')
# else: print('not found')
# print(idList)


id = input('Enter doctor ID: ')

sql = 'SELECT name FROM doctor where id = \"' + id +'\"'
mycursor.execute(sql)
name = mycursor.fetchone()

func(name)




# # if checkTableExists(hdl, "donation_types") == True:
# #     print("type table exists")
# # else:
# #     print("no table earlier...")
# #     mycursor.execute("""
# #         CREATE TABLE donation_types (
# #             type varchar(20) not null unique,
# #             frequency_days integer not null,
# #             primary key(type)
# #         )
# #         """)
# #     mycursor.execute("""
# #         INSERT INTO donation_types (type, frequency_days) VALUES
# #         ("Blood", 54),
# #         ("Platelets", 7),
# #         ("Plasma", 28),
# #         ("Power Red", 112)
# #         """)
# #     print("now created")

# # print("________")

# # if checkTableExists(hdl, "donation") == True:
# #     print("donation table exists")
# # else:
# #     print("no table earlier...")
# #     mycursor.execute("""
# #         CREATE TABLE donation (
# #             name varchar(20) not null,
# #             amount_donated_CC decimal(5,2) not null,
# #             donationDate date,
# #             donation_type text not null references donation_types(type)
# #         )
# #         """)
# #     print("now created")


# # if hdl is not None and hdl.is_connected():
# #     hdl.close()
# #     print('Connection closed.')


# # # mycursor.execute(
# # #         "CREATE TABLE bloodbank (name VARCHAR(255), address VARCHAR(255))")

# # # sql = "select * from customers"
# # # mycursor.execute(sql)
# # # data=mycursor.fetchall()
# # # for row in data:
# # #     if row[0]=="Archit":
# # #         print(row[1])


# # # sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
# # # val = ("Archit", "Delhi")
# # # mycursor.execute(sql, val)
# # # hdl.commit()

# # # mycursor.execute(
# # #     "CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")

# # # IF EXISTS (SELECT 1
# # #            FROM INFORMATION_SCHEMA.TABLES
# # #            WHERE TABLE_TYPE='BASE TABLE'
# # #            AND TABLE_NAME='mytablename')
# # #    SELECT 1 AS res ELSE SELECT 0 AS res;

# # # IF EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_NAME='mytablename')
