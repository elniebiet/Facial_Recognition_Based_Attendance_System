import pymysql
from tkinter import *

class ViewCourse():
    def getCourseDetails(self, connection, courseCode):
#         connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
        try:
            cursor = connection.cursor()
            query = f"SELECT * FROM courses WHERE coursecode = '{courseCode}' ;"
            cursor.execute(query)
            courseDet = list()
            count = 0
            data = cursor.fetchall()
            for d in data:
                courseDet.append(d)  
    #             print(data[count])
                count = count+1    
            connection.commit()
            connection.close()
            count = 0
    #         print(deptList)
            return courseDet
        except pymysql.err.InternalError:
            connection.rollback()
            connection.close()
            messagebox.showinfo("Response", "1. Error fetching course details")
            return 1 #not used
        else:
            connection.rollback()
            connection.close()
            messagebox.showinfo("Response", "2. Error  fetching course details")
            return 2 #not used 
    def getTotalStudents(self, connection, courseCode):
#         connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
        try:
            cursor = connection.cursor()
            query = f"SELECT * FROM {courseCode} ;"
            cursor.execute(query)
            connection.commit()
            count = cursor.rowcount
            connection.close()
    #         print(deptList)
            return count
        except pymysql.err.InternalError:
            connection.rollback()
            connection.close()
            messagebox.showinfo("Response", "1. Error fetching course details")
            return ''
        else:
            connection.rollback()
            connection.close()
            messagebox.showinfo("Response", "2. Error  fetching course details")
            return '' 