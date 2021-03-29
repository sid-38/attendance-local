import requests
from config import *
while(1):
    choice = input("Menu\n1. Enroll\n2. Mark attendance\n3. Exit\n Enter your choice: ")
    if choice == "1":
        #Enrollment
        _id = input("Please enter id: ")
        fp = input("Enter {} elements of fp seperated by space: ".format(n)).split()[:n]
        fp_int = [int(x) for x in fp]
        # print(fp_int)
        response = requests.post("http://localhost:5000/api/enroll",json={"id":_id, "fp":fp_int})
        if response.status_code == requests.codes.ok:
            print("Successfully enrolled!")
        else:
            print("Error!")
    elif choice == "2":
        #Marking attendance
        fp = input("Enter {} elements of fp seperated by space: ".format(n)).split()[:n]
        fp_int = [int(x) for x in fp]
        response = requests.post("http://localhost:5000/api/verify",json={"fp":fp_int})
        if response.status_code == requests.codes.ok:
            print("Attendance has been marked!")
        elif response.status_code == 403:
            print("Fingerprint not found!")
        else:
            print(type(response.status_code))
            print("Error!")
    elif choice == "3":
        break
    else:
        print("Invalid choice")