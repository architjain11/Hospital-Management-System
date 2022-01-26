# import datetime

import mysql.connector
from mysql.connector import Error

def checkTableExists(tablename):
    mycursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if mycursor.fetchone()[0] == 1:
        return True
    return False


hdl = None
try:
    hdl = mysql.connector.connect(
        host="mysqlServer", port="3306", user="root", passwd="password", database="project")
    mycursor = hdl.cursor()
    if hdl.is_connected():
        print('Successfully connected to MySQL database')
except:
    print(Error)

if checkTableExists("donation_types") == True:
    pass
else:
    print("no table earlier...")
    mycursor.execute("""
        CREATE TABLE donation_types (
            type varchar(20) not null unique,
            frequency_days integer not null,
            primary key(type)
        )
        """)
    mycursor.execute("""
        INSERT INTO donation_types (type, frequency_days) VALUES
        ("Blood", 54),
        ("Platelets", 7),
        ("Plasma", 28),
        ("Power Red", 112)
        """)

if checkTableExists("donation") == True:
    pass
else:
    print("no table earlier...")
    mycursor.execute("""
        CREATE TABLE donation (
            name varchar(20) not null,
            amount_donated_CC decimal(5,2) not null,
            donationDate date,
            donation_type text not null references donation_types(type)
        )
        """)



print("_____________________________________")
print("WELCOME TO HOSPITAL MANAGEMENT SYSTEM")
print("_____________________________________")
print(" 1 --> Hospital Staff")
print(" 2 --> Doctor")
print(" 3 --> Patient")
print(" 4 --> Blood Bank/Blood Donation")
print(" 5 --> End Program")
print("_____________________________________")

choice = int(input("Enter your choice- "))

while choice!=5:
    pass

print("Wish you health. Take Care. Bye")

if hdl is not None and hdl.is_connected():
    hdl.close()
    print('Connection closed.')