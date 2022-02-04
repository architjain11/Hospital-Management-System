import mysql.connector
from mysql.connector import Error
from stdiomask import getpass

# function to check if our table already exists in the SQL database or not
def checkTableExists(tablename):
    mycursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if mycursor.fetchone()[0] == 1:
        return True
    return False


# connect to MySQL using mysqlconnector and display whether connected successfully or not
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

# below blocks call checkTableExists function to check if tables already exist in SQL database. if yes, it does nothing. and i the tables don't exist, then those tables are created

# checks if donation_types table exists or not which has the information about how many days to wait until the donor can donate again
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

# checks if donation table exists or not which has data of everyone who has donated
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

# checks if donate table exists or not which has data of everyone who wants to volunteer as a donor
if checkTableExists("donate") == True:
    pass
else:
    mycursor.execute("""
        CREATE TABLE donate (
            name varchar(20) not null,
            donationDate date,
            donation_type text not null,
            mail varchar(50),
            reason varchar(200)
        )
        """)

# checks if login table exists or not which has the login information of staff members
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
            ("sj001", "admin")
        """)
    hdl.commit()

# checks if doctor table exists or not which has information about all the doctors at the hospital
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

# checks if beds table exists or not which has information about the total number of beds and the number of beds available in the hospital
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

# checks if appointments table exists or not which has information about the all the appointments scheduled
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

# below are the menu declarations that are called if and when required

# displays the main menu options


def mainMenu():
    print("_____________________________________")
    print(" 1 --> Hospital Staff")
    print(" 2 --> Doctor")
    print(" 3 --> Patient")
    print(" 4 --> Blood Bank/Blood Donation")
    print(" 5 --> Check availability of beds")
    print(" 6 --> End Program")
    print("_____________________________________")

# displays staff menu options


def staffMenu():
    print("_____________________________________")
    print(" 1 --> Modify beds available")
    print(" 2 --> Add new doctor")
    print(" 3 --> Remove doctor")
    print(" 4 --> Create new staff login")
    print(" 5 --> Remove staff login")
    print(" 6 --> Reset all appointments")
    print(" 7 --> Add new donation information to bank")
    print(" 8 --> View list of potential donors")
    print(" 9 --> Change your password")
    print(" 10 --> Go back to Main Menu")
    print("_____________________________________")

# displays doctor menu options


def docMenu(name):
    print("_____________________________________")
    print('Welcome ' + name)
    print('1 --> Mark available for today')
    print('2 --> Mark unavailable for today')
    print('3 --> View your appointments')
    print('4 --> Go back to Main Menu')
    print("_____________________________________")

# displayed blood bank menu options


def bbMenu():
    print("_____________________________________")
    print('1 --> Sign up for donation')
    print('2 --> Check availability in blood bank')
    print('3 --> Go back to Main Menu')
    print("_____________________________________")


print("_____________________________________")
print("WELCOME TO HOSPITAL MANAGEMENT SYSTEM")
mainMenu()

choice = int(input("Enter your choice- "))

# runs the while loop until the user selects the option to exit the program
while choice != 6:
    # staff login
    if choice == 1:
        print("_____________________________________")
        id = input('ID: ')
        pwd = getpass(prompt='Password: ')

        mycursor.execute("SELECT * FROM login")
        idList = mycursor.fetchall()

        # staff menu functionality is available only when the correct id-password pair is entered
        if (id, pwd) in idList:
            staffMenu()
            staff_choice = int(input("Enter your choice- "))

            # staff menu is looped until the user selects the option to go back to main menu
            while staff_choice != 10:
                # to modify the number of beds available
                if staff_choice == 1:
                    beds = input('How many beds are available now? ')
                    sql = "UPDATE beds SET available = " + beds + " WHERE data= \"Available Beds\""
                    mycursor.execute(sql)
                    hdl.commit()
                    print("Number of beds available modified to " +
                          beds + ". Going back to Staff Menu")

                # to add a new doctor to the doctor's list
                elif staff_choice == 2:
                    doc_info = list()
                    doc_info.append(input('Enter doctor ID: '))
                    doc_info.append(input('Enter doctor name: '))
                    doc_info.append(input('Enter doctor specialization: '))
                    sql = "INSERT INTO doctor VALUES (%s, %s, %s, 0)"
                    mycursor.execute(sql, doc_info)
                    hdl.commit()
                    print('New doctor added to database, going back to Staff Menu')

                # to remove a doctor from database
                elif staff_choice == 3:
                    id = input('Enter doctor ID to be removed: ')
                    sql = "SELECT id from doctor"
                    mycursor.execute(sql)
                    idList = mycursor.fetchall()
                    if (id,) in idList:
                        sql = "DELETE FROM doctor WHERE id = \"" + id + "\""
                        mycursor.execute(sql)
                        hdl.commit()
                        print("Doctor ID " + id +
                            " removed from database, going back to Staff Menu")
                    else:
                        print('Invalid ID, going back to Staff Menu')

                # to add new staff login ID
                elif staff_choice == 4:
                    staff_info = list()
                    staff_info.append(input('Enter new staff ID: '))
                    staff_info.append(input('Enter new staff password: '))
                    sql = "INSERT INTO login VALUES (%s, %s)"
                    mycursor.execute(sql, staff_info)
                    hdl.commit()
                    print('New staff login created, going back to Staff Menu')

                # to remove an existing staff ID
                elif staff_choice == 5:
                    id = input('Enter staff ID to be removed: ')
                    sql = "SELECT id from login"
                    mycursor.execute(sql)
                    idList = mycursor.fetchall()
                    if (id,) in idList:
                        sql = "DELETE FROM login WHERE id = \"" + id + "\""
                        mycursor.execute(sql)
                        hdl.commit()
                        print("Staff ID " + id +
                            " removed from database, going back to Staff Menu")
                    else:
                        print('Invalid ID, going back to Staff Menu')

                # to clear out all appointments for the day in the database
                elif staff_choice == 6:
                    ans = input(
                        'Are you sure you want to reset all appointments? y/n: ')
                    if ans == 'y' or ans == 'Y':
                        sql = "DELETE FROM appointments"
                        mycursor.execute(sql)
                        hdl.commit()
                        print('All older appointments are now removed')
                    print('Going back to Staff Menu')

                # to add information about donation for blood bank
                elif staff_choice == 7:
                    donation_info = list()
                    donation_info.append(input('Enter name: '))
                    donation_info.append(
                        input('Enter amount of blood donated in CC (upto two decimal values): '))
                    donation_info.append(input('Donation date (yyyy-mm-dd): '))
                    print(
                        'Select donation type:\n1. Blood\n2. Platelets\n3. Plasma\n4. Power Red')
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
                    print('Added new donation to bank, going back to Staff Menu')

                # to view list of potential donors who signed up
                elif staff_choice == 8:
                    sql = "SELECT * FROM donate"
                    mycursor.execute(sql)
                    data = mycursor.fetchall()
                    if mycursor.rowcount != 0:
                        print(
                            '(\'Name\', \'Date preferred\', \'Donation Type\', \'Mail\', \'Reason\')')
                        for row in data:
                            print(row)
                    else:
                        print('No potential donors available')
                    print('Going back to Staff Menu')

                # to change password for login ID
                elif staff_choice == 9:
                    current = getpass(prompt='Enter current password: ')
                    if current == pwd:
                        new0 = getpass(prompt='Enter new password: ')
                        new1 = getpass(prompt='Confirm new password: ')
                        if new0 == new1:
                            sql = "UPDATE login SET password = \"" + new0 + "\" WHERE id = \"" + id + "\""
                            mycursor.execute(sql)
                            hdl.commit()
                            pwd = new0
                            print('Password updated, going back to Staff Menu')
                        else:
                            print(
                                'Password does not match, going back to Staff Menu')
                    else:
                        print(
                            'Incorrect current password, try again. Going back to Staff Menu')
                else:
                    print('Incorrect Choice, going back to Staff Menu')

                staffMenu()
                staff_choice = int(input("Enter your choice- "))
            print('Opening Main Menu')
        else:
            print('Incorrect login details, going back to Main Menu')

    # doctor login
    elif choice == 2:
        print("_____________________________________")
        id = input('Enter doctor ID: ')
        mycursor.execute("SELECT id FROM doctor")
        idList = mycursor.fetchall()

        # doctor menu functionality is available only when the correct ID is entered
        if (id,) in idList:
            sql = 'SELECT name FROM doctor where id = \"' + id + '\"'
            mycursor.execute(sql)
            name = mycursor.fetchone()[0]
            docMenu(name)
            doc_choice = int(input("Enter your choice- "))
            while doc_choice != 4:
                # mark doctor available for the day
                if doc_choice == 1:
                    sql = "UPDATE doctor SET available_today = 1 WHERE id= \"" + id + "\""
                    mycursor.execute(sql)
                    hdl.commit()
                    print('You are marked available now, going back to Doctor Menu')

                # mark doctor unavailable for the day
                elif doc_choice == 2:
                    sql = "UPDATE doctor SET available_today = 0 WHERE id= \"" + id + "\""
                    mycursor.execute(sql)
                    hdl.commit()
                    print('You are marked unavailable now, going back to Doctor Menu')

                # view the list of patients who scheduled their appointments with the doctor
                elif doc_choice == 3:
                    sql = "SELECT name, age, symptoms FROM appointments where doc_id = \"" + id + "\""
                    mycursor.execute(sql)
                    data = mycursor.fetchall()
                    if mycursor.rowcount != 0:
                        print('(\'Name\', \'Age\', \'Symptoms\')')
                        for row in data:
                            print(row)
                        print('Going back to Doctor Menu')
                    else:
                        print('No appointments found, going back to Doctor Menu')
                else:
                    print('Incorrect Choice, going back to Doctor Menu')
                docMenu(name)
                doc_choice = int(input("Enter your choice- "))
            print('Opening Main Menu')
        else:
            print('ID not found, going back to Main Menu')

    # add a new appointment
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

    # sign up as a donor or check blood bank availability data
    elif choice == 4:
        bbMenu()
        bb_choice = int(input("Enter your choice- "))

        # blood bank functionality is available only when correct option is entered in the choice
        while bb_choice != 3:
            # sign up as a donor
            if bb_choice == 1:
                donate_info = list()
                donate_info.append(input('Enter name: '))
                donate_info.append(
                    input('Enter preferred date (yyyy-mm-dd): '))
                print(
                    'What do you wish to donate?\n1. Blood\n2. Platelets\n3. Plasma\n4. Power Red')
                found = False
                while(found != True):
                    don_type = int(input('Enter option number: '))
                    if don_type == 1:
                        donate_info.append('Blood')
                        found = True
                    elif don_type == 2:
                        donate_info.append('Platelets')
                        found = True
                    elif don_type == 3:
                        donate_info.append('Plasma')
                        found = True
                    elif don_type == 4:
                        donate_info.append('Power Red')
                        found = True
                    else:
                        print('Invalid choice, enter again')
                donate_info.append(input('Enter email for contact: '))
                donate_info.append(
                    input('Is there a reason for donation (if any): '))
                sql = "INSERT INTO donate VALUES (%s, %s, %s, %s, %s)"
                mycursor.execute(sql, donate_info)
                hdl.commit()

                sql = 'SELECT frequency_days FROM donation_types WHERE type = \'' + \
                    donate_info[2] + '\''
                mycursor.execute(sql)
                freq = mycursor.fetchone()[0]
                print('Thank You, ' + donate_info[0] + '.')
                print(
                    f'NOTE: You can donate {donate_info[2]} only ONCE in {freq} days.')
                print(
                    'We will contact you for confirmation via email, going back to Main Menu')

            # view the availablity status in the blood bank
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
            else:
                print('Incorrect Choice, going back to Main Menu')

            bbMenu()
            bb_choice = int(input("Enter your choice- "))
        print('Opening Main Menu')

    # displays the current bed availability in the hospital
    elif choice == 5:
        sql = "SELECT * FROM beds"
        mycursor.execute(sql)
        data = mycursor.fetchall()
        print(f"Number of total beds: {data[0][1]}")
        print(f"Number of beds available: {data[1][1]}")
        print('Going back to Main Menu')

    else:
        print('Incorrect Choice, try again')

    mainMenu()
    choice = int(input("Enter choice to continue- "))

print("Wish you health. Take Care. Bye")

# the sql connection is closed
if hdl is not None and hdl.is_connected():
    hdl.close()
    print('MySQL Connection closed.')