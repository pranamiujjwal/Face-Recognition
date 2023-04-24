#Program to create a file full of known faces encodes
import os
import re
from typing import final
import cv2
import json
import numpy
import pickle
import getpass
import smtplib
import mimetypes
import subprocess
import face_recognition
from email.message import EmailMessage

class Main:  
    def __init__(self):
        """Constructor"""
        if os.path.exists("DB") == 0:
            print("Error: Files not found")
            if input("Want to run setup?(Y/N): ").lower()=='y' :
                print("Running Setup Program")
                self.Setup()
                os.system("cls")
            else:
                print("Program Terminated, error: file not found!")
                return
        if os.path.getsize("DB")>0:
            with open("DB", "rb") as file:
                self.db=pickle.loads(file.read())
                file.close()
        else:
            self.db={}

    def Setup(self):
        """Setup()"""
        # # part 1: Install all required libraries 
        # subprocess.run("pip install -r {}".format("requirements.txt"))
        # os.system("cls")    
        # print("All Libraries Installed")
        # part 2: Create A binary file to hold user creadiantials
        
        if os.path.exists("users"):
            print("User file found Cannot creat new file")
        else:
            print("Your Username is: 1")
            name=input("Enter your name: ")
            pswrd0=input("Enter your password: ")
            pswrd1=input("Confirm your password: ")
            if pswrd0==pswrd1:
                data={1:[pswrd0, name]}
                with open("users", "wb") as file:
                    file.write(pickle.dumps(data))
                    file.close()
                print("user file generated")
            else:
                print("Password not matched")
        # part 3: Create A binary file to hold defaulters name
        if os.path.exists("DB"):
            print("User file found Cannot creat new file")
        else:
            with open("DB", "wb") as file:
                data={"Enrollment":0}
                file.write(pickle.dumps(data))
                file.close()
                print("DB file generated")
        print("setup Completed!")
        input("Press any key to continue.....") 
    
    def Login(self):
        """Login("users"= "string"):"""
        with open("users", "rb") as file:
            data=pickle.loads(file.read())
            # print(data)
            file.close()
        usr=int(input("Enter Username: "))
        if usr in data.keys():
            pswrd=input("{}, Enter your Password: ".format(data[usr][1]))
            if pswrd==data[usr][0]:
                self.Welcome()
                # print("welcome", data[usr][1])
        else:
            print("Username not found")
            input("Press any key to continue.....")
    
    def Welcome(self):
        """welcome"""
        os.system("cls")
        print("welcome Sir")
        print("Operations:")
        print("1. Enroll Face")
        print("2. Show Details")
        print("3. Show Report")
        print("4. Update Report")
        print("5. Email Report")

        choice = int(input("Your Choice: "))
        if choice == 1:
            """Enroll face"""
            print("Enrolling Face")
            self.chose_file()
        elif choice == 2:
            """Show Details"""
            print("Show Details")
            parameter = input("enter parameter: ")
            self.show(parameter)
        elif choice == 3:
            """Show Database"""
            print("Show Database")
            self.ShowDB()
        elif choice == 4:
            """update db"""
            self.UpdateDB()
        elif choice == 5:
            """Send Report as Email"""
            self.DesignMail()
        else:
            print("wrong choice!")
            input("press any key to continue.....")
    
    def chose_file(self):
        """select file"""
        os.system("cls")
        print("\nAdding known faces:")
        path = input("Enter the path of folder/path: ")
        path = re.sub(r"\\", '/', path)
        path += '/'
        while os.path.isdir(path):
            i = 0
            os.system("cls")
            print("current path: ", path)
            files = os.listdir(path)
            for file in files:
                i += 1
                print(f"{i}. {file}")
            choice = int(input(("select files:(in numeric): ")))
            try:
                path = path+'/'+files[choice-1]
            except:
                print("choice not pic not found")
            finally:
                print(f'path of file is :{path}')
        self.add_face(path)  

    def add_face(self, path):
        """add face to binary file"""
        #known='D:/VS code/python/Projects/known'
        try:
            with open("known", "rb") as file:
                # extract all nown encodes from the file
                data = pickle.loads(file.read())
                file.close()
                i = 0
                for value in data.values():
                    i += 1
        except:
            data = {}
            i = 0
        match = re.search(r'\.jpg$', path)
        if match is None:
            print("file not supported")
            return
        else:
            name = re.sub(r'\.jpg', '', path)
            name = re.search(r"[^\/]+$", name)
            name = name.group()
            print(name)
            image = face_recognition.load_image_file(path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(image)[0]
            # generating a dictionary with key value 'i',  
            # and with value consisting of a list[encode,name]
            data.update({i: [encode, name]})
            f = open("known", "wb")
            f.write(pickle.dumps(data))
            f.close()
            print('Entery number: ', i)
            print('Face enrolled')
            input("press any key to continue.....")

    def ReadFace(self):
        """open image file for recognition"""
        #known='D:/VS code/python/Projects/known'
        known='known'
        with open(known, 'rb') as file:
            # extract all nown encodes from the file
            data = pickle.loads(file.read())  
            file.close()
        knownfacesencodes = []
        name = []
        for i in data.values():
            knownfacesencodes.append(i[0])
            name.append(i[1])

        roll = []
        files = os.listdir("Found")
        for file in files:                
            # load testimage
            testimage = face_recognition.load_image_file("Found/"+file)  
            # convert testimage
            testimage = cv2.cvtColor(testimage, cv2.COLOR_BGR2RGB)
            # testface location
            testimagefacelocation = face_recognition.face_locations(testimage)
            # test face encodes
            testimagefaceencoding = face_recognition.face_encodings(testimage)  
            #comparing both image encodes for similarities
            for encodes, face in zip(testimagefaceencoding, testimagefacelocation):
                result = face_recognition.compare_faces(knownfacesencodes, encodes)
                facedistance = face_recognition.face_distance(
                    knownfacesencodes, 
                    encodes
                )
                matchindex = numpy.argmin(facedistance)
                if result[matchindex]:
                    roll.append(name[matchindex])
        # print(roll)
        return roll
             
    def details(self, parameter):  
        """read student data and return selected student details"""  
        # datafile="D:/VS code/python/Projects/student_details.json"
        try:
            with open("Myfile1.json", "r") as rf:
                decoded_data = json.load(rf)
        except:
            return None
        try:
            student_data = decoded_data[parameter]
            # print(student_data)
            return student_data
        except KeyError:
            return 1

    def show(self, parameter):
        """takes enrollment number as input and show output"""
        os.system("cls")
        student_data = self.details(parameter.upper())
        if student_data == None:
            print("Oops! JSON Data not loaded correctly using json.loads()")
            input("press any key to continue.....")
        elif student_data == 1:
            print("parameter not found in dictionary")
            input("press any key to continue.....")
        else:        
            print("Enrollment Number.:{}".format(parameter.upper()))
            print("Name:{}".format(student_data["name"]))
            print("Branch:{}".format(student_data["branch"]))
            print("Semester:{}".format(student_data["semester"]))
            print("Address:{}".format(student_data["address"]))
            print("Age:{} years".format(student_data["age"]))
            input("press any key to continue.....") 
    
    def UpdateDB(self):
        print("please wait while updating DB.....")
        roll = self.ReadFace()       # Recognize all faces from "Found" folder
        self.NoteNames(roll)
        self.DeleteCache()
        print("Updating Completed")
        
    def ShowDB(self):
        print("Enrollment   \t Value")
        for key in self.db.keys():
            if key != "Enrollment":
                print(key, "\t", self.db[key])
    
    def DeleteCache(self):
        """"""
        files = os.listdir("Found")
        if len(files)>0:
            for file in files: 
                os.remove(file)

    def SaveDatabase(self):
        """save dict to binary file "DB"""
        print(self.db)
        with open("DB", "wb") as file:
            file.write(pickle.dumps(self.db))
            print("DB saved sucessfullly")
            file.close()
        
    def NoteNames(self, keys):
        """increment value of dict if student found without mask"""
        for key in keys:
            if key in self.db.keys():
                if self.db[key]>10:
                    self.db[key]=1
                else:
                    self.db[key]+=1
            else:
                self.db[key]=1

    def DesignMail(self):
        mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
        sender = "xyz@gmail.com"
        # mail_pass = "*********"
        print("User: ", sender)
        mail_pass = getpass.getpass('Password: ')

        try:
            mail_server.login(sender, mail_pass)
        except:
            print("Login failed")
            return

        message = EmailMessage()
        recipients="pranamiujjwal0000@gmail.com"
        other_recipients = [
            "pranamiujjwal2001@gmail.com",
        ]

        message['From'] = sender
        message['To'] = recipients
        message['Cc'] = other_recipients
        # msg['Bcc'] = they
        message['Subject'] = 'Report of Students Without Mask '
        body="""List of Students found without Mask \nEnrollment    \tValue \n"""
        for key in self.db.keys():
            if key != "Enrollment":
                body+="{}\t{} \n".format(key, self.db[key])
        body+="\nRespective Tg's Inform Students to wear mask in college campus"
        message.set_content(body)

        # print(message)
        try:
            if input("Do you want to send this Email(Y/N): ").lower()=='y':
                mail_server.send_message(message)
                print("Email sent to '{}' sucessfully".format(message['To']))
            else:
                print("EMail not sent")
        except:
                print("Exceptin occured! Email not sent")
        finally:
            mail_server.quit()

    def __del__(self):
        """save dict to binary file "DB"""
        with open("DB", "wb") as file:
            file.write(pickle.dumps(self.db))
            file.close()
        input("press any key to continue.....")



if __name__ == "__main__":
    """Main Program For Project"""
    M = Main()
    print("Operations:")
    print("1. Login")
    print("2. Setup")
    print("3. Report")
    print("4. Email Report")

    choice = int(input("Your Choice: "))
    if choice == 1:
        M.Login()
    elif choice == 2:
        M.Setup()
    elif choice == 3:
        M.ShowDB()
    elif choice == 4:
        M.DesignMail()
    else:
        print("wrong choice!")
    del M