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
    print('Could not connect to MySQL Server')
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
    print(" 4 --> Create new staff login")
    print(" 5 --> Remove staff login")
    print(" 6 --> Change your password")
    print(" 7 --> Go back to Main Menu")
    print("_____________________________________")


print("_____________________________________")
print("WELCOME TO HOSPITAL MANAGEMENT SYSTEM")
mainMenu()

choice = int(input("Enter your choice- "))

while choice != 5:
    if choice == 1:
        print("_____________________________________")
        id = input('ID: ')
        pwd = getpass(prompt='Password: ')

        mycursor.execute("SELECT * FROM login")
        idList = mycursor.fetchall()

        if (id, pwd) in idList:
            staffMenu()
            staff_choice = int(input("Enter your choice- "))
            if staff_choice == 1:
                beds = input('How many beds are available now? ')
                sql = "UPDATE beds SET available = " + beds + " WHERE data= \"Available Beds\""
                mycursor.execute(sql)
                hdl.commit()
                print("Number of beds available modified to " + beds)

            elif staff_choice == 2:
                doc_info = list()
                doc_info.append(input('Enter doctor ID: '))
                doc_info.append(input('Enter doctor name: '))
                doc_info.append(input('Enter doctor specialization: '))
                sql = "INSERT INTO doctor VALUES (%s, %s, %s, 0)"
                mycursor.execute(sql, doc_info)
                hdl.commit()
                print('New doctor added to database, going back to Main Menu')

            elif staff_choice == 3:
                id = input('Enter doctor ID to be removed: ')
                sql = "DELETE FROM doctor WHERE id = \"" + id + "\""
                mycursor.execute(sql)
                hdl.commit()
                print("Doctor ID " + id + " removed from database, going back to Main Menu")

            elif staff_choice == 4:
                staff_info = list()
                staff_info.append(input('Enter new staff ID: '))
                staff_info.append(input('Enter new staff password: '))
                sql = "INSERT INTO login VALUES (%s, %s)"
                mycursor.execute(sql, staff_info)
                hdl.commit()
                print('New staff login created, going back to Main Menu')

            elif staff_choice == 5:
                id = input('Enter staff ID to be removed: ')
                sql = "DELETE FROM login WHERE id = \"" + id + "\""
                mycursor.execute(sql)
                hdl.commit()
                print("Staff ID " + id + " removed from database, going back to Main Menu")

            elif staff_choice == 6:
                current = getpass(prompt='Enter current password: ')
                if current == pwd:
                    new0 = getpass(prompt='Enter new password: ')
                    new1 = getpass(prompt='Confirm new password: ')
                    if new0 == new1:
                        sql = "UPDATE login SET password = \"" + new0 + "\" WHERE id = \"" + id + "\""
                        mycursor.execute(sql)
                        hdl.commit()
                        print('Password updated, going back to Main Menu')
                    else:
                        print('Password does not match, going back to Main Menu')
                else:
                    print('Incorrect password, going back to Main Menu')

            elif staff_choice == 7:
                print('Opening Main Menu')

            else:
                print('Incorrect Choice, going back to Main Menu')
        else:
            print('Incorrect login details, going back to Main Menu')

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
