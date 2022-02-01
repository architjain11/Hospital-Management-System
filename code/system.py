# import datetime

import mysql.connector
from mysql.connector import Error
from getpass import getpass


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
    exit()

if checkTableExists("donation_types") == True:
    pass
else:
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
    hdl.commit()


if checkTableExists("donation") == True:
    pass
else:
    mycursor.execute("""
        CREATE TABLE donation (
            name varchar(20) not null,
            amount_donated_CC decimal(5,2) not null,
            donationDate date,
            donation_type text not null references donation_types(type)
        )
        """)

if checkTableExists("login") == True:
    pass
else:
    mycursor.execute("""
        CREATE TABLE login (
            id varchar(20) not null,
            password varchar(50) not null
        )
        """)
    mycursor.execute("""
        INSERT INTO login (id, password) VALUES
            ("sj001", "password")
        """)
    hdl.commit()

if checkTableExists("doctor") == True:
    pass
else:
    mycursor.execute("""
        CREATE TABLE doctor (
            id varchar(20) not null,
            name varchar(50) not null,
            specialization varchar(50),
            available_today int
        )
        """)

if checkTableExists("beds") == True:
    pass
else:
    mycursor.execute("""
        CREATE TABLE beds (
            data varchar(20) not null,
            available int not null
        )
        """)
    mycursor.execute("""
        INSERT INTO beds (data, available) VALUES
            ("Total Beds", "200"),
            ("Available Beds", "140")
        """)
    hdl.commit()

if checkTableExists("appointments") == True:
    pass
else:
    mycursor.execute("""
        CREATE TABLE appointments (
            name varchar(20) not null,
            age int not null,
            doc_id varchar(20),
            symptoms varchar (200)
        )
        """)


def mainMenu():
    print("_____________________________________")
    print(" 1 --> Hospital Staff")
    print(" 2 --> Doctor")
    print(" 3 --> Patient")
    print(" 4 --> Blood Bank/Blood Donation")
    print(" 5 --> End Program")
    print("_____________________________________")

def staffMenu():
    print("_____________________________________")
    print(" 1 --> Modify beds available")
    print(" 2 --> Add new doctor")
    print(" 3 --> Remove doctor")
    print(" 4 --> Change your password")
    print(" 5 --> Go back to Main Menu")
    print("_____________________________________")


print("_____________________________________")
print("WELCOME TO HOSPITAL MANAGEMENT SYSTEM")
mainMenu()

choice = int(input("Enter your choice- "))

while choice != 5:
    if choice == 1:
        print("_____________________________________")
        id = input('ID: ')
        val = list()
        val.append(id)
        pwd = getpass(prompt='Password: ')
        sql = "SELECT password FROM login WHERE id = %s"
        mycursor.execute(sql, val)
        data = mycursor.fetchone()
        if pwd in data:
            staffMenu()
            staff_choice = int(input("Enter your choice- "))
            if choice == 1:
                beds = input('How many beds are available now? ')
                sql = "UPDATE beds SET available = " + beds + " WHERE data= \"Available Beds\""
                mycursor.execute(sql)
                hdl.commit()
                print("Number of beds available modified to " + beds)
            
            if choice == 2:
                pass
            
            if choice == 3:
                pass
            
            if choice == 4:
                pass
        else:
            'Incorrect Password, going back to Main Menu'

    elif choice == 2:
        pass
        # mark available for today or mark unavailable

    elif choice == 3:
        pass

    elif choice == 4:
        pass

    else:
        print('Incorrect Choice, going back to Main Menu')

    mainMenu()
    choice = int(input("Enter choice to continue- "))


print("Wish you health. Take Care. Bye")

if hdl is not None and hdl.is_connected():
    hdl.close()
    print('Connection closed.')
