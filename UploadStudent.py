import pymysql
from tkinter import *
from shutil import copyfile
class UploadStudent():
    def upload(self, connection, idnumber, firstname, lastname, department, imagename):
#         connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
        try:
            cursor = connection.cursor()            
            query = f"INSERT INTO students (idnumber, firstname, lastname, department, imagename) VALUES ('{idnumber}', '{firstname}', '{lastname}', '{department}', '{imagename}');"
            print(query)
            cursor.execute(query)
            connection.commit()
            connection.close()
            #move images to folder
            try:
                copyfile("ImgReg.png", "students/"+imagename)
                copyfile("ResizedImgReg.png", "students/"+"Resized"+imagename)
            except: 
                messagebox.showinfo("Response", "Error saving images")
            messagebox.showinfo("Response ", idnumber+" registered successfully.")
            return 0
        except pymysql.err.IntegrityError: 
            connection.close()
            messagebox.showinfo("Response", "idnumber: "+idnumber+", already exists.")
            return 1
        except pymysql.err.InternalError:
            connection.close()
            messagebox.showinfo("Response", "idnumber: "+idnumber+", already exists.")
            return 1
        except pymysql.err.ProgrammingError:
            connection.close()
            messagebox.showinfo("Response", "Please supply valid data")
            return 1
        else:
            connection.close()
            messagebox.showinfo("Response", "Error Adding Student")
            return 2