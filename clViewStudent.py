import pymysql
from tkinter import *

class ViewStudent():
    def getStudents(connection, courseName):
#         connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
        if courseName == 'select':
            messagebox.showinfo("Response", "No course selection has been made")
            return
        try:
            cursor = connection.cursor()
            query = f"SELECT studentid,total_attendance FROM {courseName} INNER JOIN students ON {courseName}.studentid = students.idnumber;"
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
    #         print(deptList)
            return stList
        except pymysql.err.InternalError:
            connection.close()
            messagebox.showinfo("Response", "Error loading students")
            return 1 #not used
        else:
            connection.close()
            messagebox.showinfo("Response", "Error  loading students")
            return 2 #not used 
    def getStudentsFromDept(connection, deptName):
#         connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
        if deptName == 'select':
            messagebox.showinfo("Response", "No course selection has been made")
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
            print("student list from view student is: ")
            print(stList)
            return stList
        except pymysql.err.InternalError:
            connection.close()
            messagebox.showinfo("Response", "Error loading students")
            return 1 #not used
        else:
            connection.close()
            messagebox.showinfo("Response", "Error Adding Course")
            return 2 #not used 
        
    def getStudentDetails(self, connection, courseName, idNumber):
        if idNumber == 'select':
            messagebox.showinfo("Response", "No student selection has been made")
            return
        try:
            cursor = connection.cursor()
            query = f"SELECT studentname, total_attendance FROM {courseName} WHERE studentid = '{idNumber}';"
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
            connection.close()
            messagebox.showinfo("Response", "Error fetching student's details")
            return 1 #not used
        else:
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
            connection.close()
            messagebox.showinfo("Response", "Error fetching student's details")
            return 1 #not used
        else:
            connection.close()
            messagebox.showinfo("Response", "Error loading students details")
            return 2 #not used
    
    def getStudentImageName(self, connection, idNumber):
        if idNumber == 'select':
#             messagebox.showinfo("Response", "No student selection has been made")
            print("select idnumber to get image name")
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
                print("Student not found")
                return ''
            else: 
                return stDetails[0][0]
        except pymysql.err.InternalError:
            connection.close()
            print("Error fetching student's image name")
            return "" #not used
        else:
            connection.close()
            print("Error fetching imagename")
            return "" #not used