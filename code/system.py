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


def docMenu(name):
    print("_____________________________________")
    print('Welcome ' + name)
    print('1 --> Mark available for today')
    print('2 --> Mark unavailable for today')
    print('3 --> View your appointments')
    print('4 --> Go back to Main Menu')
    print("_____________________________________")


def bbMenu():
    print("_____________________________________")
    print('1 --> Donate Blood')
    print('2 --> Check availability in blood bank')
    print('3 --> Go back to Main Menu')
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
                print("Doctor ID " + id +
                      " removed from database, going back to Main Menu")

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
                print("Staff ID " + id +
                      " removed from database, going back to Main Menu")

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
        print("_____________________________________")
        id = input('Enter doctor ID: ')
        mycursor.execute("SELECT id FROM doctor")
        idList = mycursor.fetchall()

        if (id,) in idList:
            sql = 'SELECT name FROM doctor where id = \"' + id + '\"'
            mycursor.execute(sql)
            name = mycursor.fetchone()[0]
            docMenu(name)
            doc_choice = int(input("Enter your choice- "))
            if doc_choice == 1:
                sql = "UPDATE doctor SET available_today = 1 WHERE id= \"" + id + "\""
                mycursor.execute(sql)
                hdl.commit()
                print('You are marked available now, going back to Main Menu')
            elif doc_choice == 2:
                sql = "UPDATE doctor SET available_today = 0 WHERE id= \"" + id + "\""
                mycursor.execute(sql)
                hdl.commit()
                print('You are marked unavailable now, going back to Main Menu')
            elif doc_choice == 3:
                sql = "SELECT name, age, symptoms FROM appointments where doc_id = \"" + id + "\""
                mycursor.execute(sql)
                data = mycursor.fetchall()
                if mycursor.rowcount != 0:
                    print('(\'Name\', \'Age\', \'Symptoms\')')
                    for row in data:
                        print(row)
                    print('Going back to Main Menu')
                else:
                    print('No appointments found, going back to Main Menu')
            elif doc_choice == 4:
                print('Opening Main Menu')
            else:
                print('Incorrect Choice, going back to Main Menu')
        else:
            print('ID not found, going back to Main Menu')

    elif choice == 3:
        print("_____________________________________")
        appointment_info = list()
        appointment_info.append(input('Enter patient name: '))
        appointment_info.append((input('Enter age: ')))
        sql = "SELECT id, name, specialization FROM doctor where available_today = 1"
        mycursor.execute(sql)
        doc_available = mycursor.fetchall()
        if mycursor.rowcount != 0:
            print('Doctors available for today: ')
            print('(\'Doctor ID\', \'Name\', \'Specialization\')')
            for row in doc_available:
                print(row)
            doc_id = input('Enter doctor ID to visit from above list: ')
            mycursor.execute("SELECT id FROM doctor where available_today = 1")
            idList = mycursor.fetchall()
            if (doc_id,) in idList:
                appointment_info.append(doc_id)
                appointment_info.append(
                    input('Explain your symptoms in brief: '))
                sql = "INSERT INTO appointments VALUES (%s, %s, %s, %s)"
                mycursor.execute(sql, appointment_info)
                hdl.commit()
                print('Appointment Scheduled, going back to Main Menu')
            else:
                print('Wrong ID, going back to Main Menu')
        else:
            print('No doctors available today, going back to Main Menu')

    elif choice == 4:
        bbMenu()
        bb_choice = int(input("Enter your choice- "))
        if bb_choice == 1:
            donation_info = list()
            donation_info.append(input('Enter name: '))
            donation_info.append(
                input('Enter amount of blood donated in CC (upto two decimal values): '))
            donation_info.append(input('Donation date (yyyy-mm-dd): '))
            print(
                'What do you want to donate?\n1. Blood\n2. Platelets\n3. Plasma\n4. Red Blood')
            found = False
            while(found != True):
                don_type = int(input('Enter option number: '))
                if don_type == 1:
                    donation_info.append('Blood')
                    found = True
                elif don_type == 2:
                    donation_info.append('Platelets')
                    found = True
                elif don_type == 3:
                    donation_info.append('Plasma')
                    found = True
                elif don_type == 4:
                    donation_info.append('Power Red')
                    found = True
                else:
                    print('Invalid choice, enter again')
            sql = "INSERT INTO donation VALUES (%s, %s, %s, %s)"
            mycursor.execute(sql, donation_info)
            hdl.commit()

            sql = 'SELECT frequency_days FROM donation_types WHERE type = \'' + \
                donation_info[3] + '\''
            mycursor.execute(sql)
            freq = mycursor.fetchone()[0]
            print('Thank You, ' + donation_info[0] + '.')
            print(f'You cannot donate again for the next {freq} days')
            print('Going back to the Main Menu')

        elif bb_choice == 2:
            sql = "SELECT donation_type, sum(amount_donated_CC) FROM donation GROUP BY donation_type"
            mycursor.execute(sql)
            data = mycursor.fetchall()
            if mycursor.rowcount != 0:
                print('(\'Donation type\', \'Amount available\')')
                for row in data:
                    print(row)
                print('Going back to Main Menu')
            else:
                print('Nothing is available right now, going back to Main Menu')
        elif bb_choice == 3:
            print('Opening Main menu')
        else:
            print('Incorrect Choice, going back to Main Menu')

    mainMenu()
    choice = int(input("Enter choice to continue- "))

print("Wish you health. Take Care. Bye")

if hdl is not None and hdl.is_connected():
    hdl.close()
    print('MySQL Connection closed.')
