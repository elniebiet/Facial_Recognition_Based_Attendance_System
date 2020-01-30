import pymysql
from tkinter import *

class EditStudent():
    def getStudentsFromDept(self, connection, deptName):
#         connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
        if deptName == 'select':
            messagebox.showinfo("Response", "No Departmant has been selected")
            return
        try:
            cursor = connection.cursor()
            query = f"SELECT idnumber FROM students WHERE department='{deptName}';"
            cursor.execute(query)
            stList = list()
            count = 0
            data = cursor.fetchall()
            for d in data:
                stList.append(d)  
    #             print(data[count])
                count = count+1    
            connection.commit()
            connection.close()
            count = 0
            return stList
        except pymysql.err.InternalError:
            connection.rollback()
            connection.close()
            messagebox.showinfo("Response", "Error loading students")
            return 1 #not used
        else:
            connection.rollback()
            connection.close()
            messagebox.showinfo("Response", "Error loading students")
            return 2 #not used 
        
    def getStudentDetails(self, connection, department, idNumber):
        if idNumber == 'select':
            messagebox.showinfo("Response", "No student selection has been made")
            return
        try:
            cursor = connection.cursor()
            query = f"SELECT idnumber, firstname, lastname, imagename FROM students WHERE idnumber = '{idNumber}';"
            cursor.execute(query)
            stDetails = list()
            count = 0
            data = cursor.fetchall()
            for d in data:
                stDetails.append(d)  
    #             print(data[count])
                count = count+1    
            connection.commit()
            connection.close()
            count = 0
    #         print(deptList)
            return stDetails
        except pymysql.err.InternalError:
            connection.rollback()
            connection.close()
            messagebox.showinfo("Response", "Error fetching student's details")
            return 1 #not used
        else:
            connection.rollback()
            connection.close()
            messagebox.showinfo("Response", "Error loading students details")
            return 2 #not used
        
    def getStudentDetailsFromDept(self, connection, courseName, idNumber):
        if idNumber == 'select':
            messagebox.showinfo("Response", "No student selection has been made")
            return
        try:
            cursor = connection.cursor()
            query = f"SELECT firstname, lastname, imagename FROM students WHERE idnumber = '{idNumber}';"
            cursor.execute(query)
            stDetails = list()
            count = 0
            data = cursor.fetchall()
            for d in data:
                stDetails.append(d)  
    #             print(data[count])
                count = count+1    
            connection.commit()
            connection.close()
            count = 0
    #         print(deptList)
            return stDetails
        except pymysql.err.InternalError:
            connection.rollback()
            connection.close()
            messagebox.showinfo("Response", "Error fetching student's details")
            return 1 #not used
        else:
            connection.rollback()
            connection.close()
            messagebox.showinfo("Response", "Error loading students details")
            return 2 #not used
    
    def getStudentImageName(self, connection, idNumber):
        if idNumber == 'select':
#             messagebox.showinfo("Response", "No student selection has been made")
#             print("select idnumber to get image name")
            return ''
        try:
            cursor = connection.cursor()
            query = f"SELECT imagename FROM students WHERE idnumber = '{idNumber}';"
            cursor.execute(query)
            stDetails = list()
            count = 0
            data = cursor.fetchall()
            for d in data:
                stDetails.append(d)  
    #             print(data[count])
                count = count+1    
            connection.commit()
            connection.close()
            count = 0
    #         print(deptList)
            if len(stDetails) == 0:
#                 print("Student not found")
                return ''
            else: 
                return stDetails[0][0]
        except pymysql.err.InternalError:
            connection.rollback()
            connection.close()
#             print("Error fetching student's image name")
            return "" #not used
        else:
            connection.rollback()
            connection.close()
#             print("Error fetching imagename")
            return "" #not used
    def checkNewIdExists(self, connection, idNumber):
        try:
            cursor = connection.cursor()
            query = f"SELECT idnumber FROM students WHERE idnumber = '{idNumber}';"
            cursor.execute(query)
            stDetails = list()
            count = 0
            data = cursor.fetchall()
            for d in data:
                stDetails.append(d)  
    #             print(data[count])
                count = count+1    
            connection.commit()
            connection.close()
            count = 0
            
            if len(stDetails) == 0: 
#                 print("ID number doesn't exists")
                return 0
            else: 
                return 1
        except pymysql.err.InternalError:
            connection.rollback()
            connection.close()
            messagebox.showinfo("Response", "1. Error checking new id")
            return "" #not used
        else:
            connection.rollback()
            connection.close()
            messagebox.showinfo("Response", "2. Error checking new id")
            return "" #not used

    def updateDetails(self, connection, idNumber, firstName, lastName):
        try:
            cursor = connection.cursor()
            query = f"UPDATE students SET firstname = '{firstName}', lastname = '{lastName}' WHERE idnumber = '{idNumber}';"
            cursor.execute(query)
            connection.commit()
            connection.close()
            return 0
        except pymysql.err.InternalError:
            connection.rollback()
            connection.close()
            messagebox.showinfo("Response", "1. Error Updating details")
            return 1
        else:
            connection.rollback()
            connection.close()
            messagebox.showinfo("Response", "2. Error Updating Details")
            return 1
    def removeStudent(self, connection, idNumber):
        try:
            cursor = connection.cursor()
            query = f"DELETE FROM students WHERE idnumber = '{idNumber}';"
            cursor.execute(query)
            connection.commit()
            connection.close()
            return 0
        except pymysql.err.InternalError:
            connection.rollback()
            connection.close()
            messagebox.showinfo("Response", "1. Error Removing Student")
            return 1
        else:
            connection.rollback()
            connection.close()
            messagebox.showinfo("Response", "2. Error Removing Student")
            return 1