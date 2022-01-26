#Project on Hospital Management

import datetime 

print("                            HOSPITAL MANAGEMENT     ")
print("Enter from the following depending on who you are and what you want --->")
print(" 1 ---> Hospital Staff")
print(" 2 ---> Doctor")
print(" 3 ---> Patient")
print(" 4 ---> Blood Bank/Blood Donation")
print(" 5 ---> End Program")

choice1 = int(input("Enter your choice "))    #Main menu choice

rooms_available=0
beds_available=0
docs = {234: 0, 345: 0}     #Keys are the unique doctor code and 0 and 1 represent absent and present for the doctor respectively
blood_bank=list()     #Blood Bank list     

while choice1!=5:     #Return back to main menu command
    
    if choice1 == 1:
        staffcode = int(input("Enter your staff code here - "))     #Staff login 
        staffpass = input("Enter your staff password here- ")
        if staffcode == 123 and staffpass == "staffpass":     #Setting the staff code and staff password
            print("                             Welcome Staff ", staffcode)
            print("Choose from the following what you would like to do")
            print(" 1 ---> Change number of rooms available")
            print(" 2 ---> Change number of beds available in the Hospital")
            print(" 3 ---> Back to Main Menu")
            
            staff_choice = int(input("Enter Staff Choice - "))     #Set the number of rooms available
            while staff_choice!=3:
                if staff_choice == 1:
                    rooms_available = int(input("Modify Current rooms available - "))
                    print("Number of rooms currently available set to = ", rooms_available)
                    
                if staff_choice == 2:     #Set the number of beds available
                    beds_available = int(input("Modify current beds available - "))
                    print("Number of beds currently available set to = ", beds_available)

                staff_choice = int(input("Enter Staff Choice again - "))
                
        else: print("Wrong Staff Credentials. Try again")


    if choice1 == 2:
        doctorcode = int(input("Enter your doctor code here - "))     #Doctor available or not marking code
        if doctorcode == 234:
            print("     Welcome Doctor Harish     ")
            print("Date:", datetime.datetime.now().strftime("%c"))
            print("   You are being marked available for today in your department ")
            print("   Thank you")
            docs[doctorcode] = 1

        elif doctorcode == 345:
            print("     Welcome Doctor Jai     ")
            print("Date:", datetime.datetime.now().strftime("%c"))
            print("   You are being marked available for today in your department ")
            print("   Thank you")
            docs[doctorcode] = 1

        else: print("Wrong Doctor ID")
            

    if choice1 == 3:     #Patient choices 
        print("Press to choose ->")
        print(" 1 ---> Make an appointment ")
        print(" 2 ---> Check number of rooms available ")
        print(" 3 ---> Check number of beds available ")
        print(" 4 ---> Back to Main Menu")


        patient_choice = int(input("Enter patient choice - "))
        while patient_choice!=4:
            if patient_choice == 1:
                name = input("Enter your name - ")
                age = input("Enter your age - ")
                print("Doctor you want to make an appointment to - ")
                print(" 1 ---> Dentist")
                print(" 2 ---> ENT")
                doctor_type = int(input("Enter what dctor you want to confirm - "))
                if doctor_type == 1:
                    if docs[234] == 1:     #If doctor is marked present/available for today then confirm appointment
                        print( name + " ,your appointment with Dr.Harish has been confirmed for time between 1 pm to 2 pm today")
                        print("consulatation fee will be 200 Rs, Thank You ")
                        print("Date:", datetime.datetime.now().strftime("%c"))
                    else: print("Sorry Dr. Harish is not available today")     #Else doctor is absent and not available today

                        
                if doctor_type == 2:
                    if docs[345] == 1:     #If doctor is marked present/available for today then confirm appointment
                        print( name + " ,your appointment with Dr.Jai has been confirmed for time between 1 pm to 2 pm")
                        print("consulatation fee will be 200 Rs, Thank You ")
                        print("Date:", datetime.datetime.now().strftime("%c"))
                    else: print("Sorry Dr. Jai is not available today")     #Else doctor is absent and not available today
                    

            if patient_choice == 2:
                print("Number of current rooms available are ", rooms_available)     #Shows the number of rooms available(set by the staff) to the patient on request

            if patient_choice == 3:
                print("Number of current beds available are ", beds_available)     #Shows the number of beds available(set by the staff) to the patient on request

            patient_choice = int(input("Enter patient choice again to continue - "))

    if choice1 == 4:     #Code to donate/check the blood bank
        print("                      Millions of people require blood every day")
        print("                        Thank you for donating to a good cause")
        print(" 1 ---> Donate")
        print(" 2 ---> Check Blood type available in bank")
        print(" 3 ---> Exit")
        choose_donate = int(input(" Enter your choice"))
        while choose_donate != 3:
            if choose_donate == 1:
                blood_group = input("Enter your blood type if you want to donate - ")
                blood_bank.append(blood_group)
                print("Date:", datetime.datetime.now().strftime("%c"))
                print("You can come anytime from 5 pm to 8 pm")
                print("Thank You")

            if choose_donate == 2:
                if not blood_bank:
                    print("No blood type available right now")
                else:
                    print("The following blood types are currently available:")
                    for type in blood_bank:
                        print(type)
                
            choose_donate = int(input("Enter blood bank menu choice again to continue - "))

            
    choice1 = int(input("Enter your Main Menu choice again to continue "))

            
print("Thanks for using my program. Bye") #Exit the program