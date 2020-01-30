import pymysql
import logging
from tkinter import *

class AddCourse():
    def createTable(self, connection, tablename, courseCode, courseTitle, courseDept, courseLecturer):
#         connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
        try:
            cursor = connection.cursor()
            query = f"CREATE TABLE {tablename} (id INT PRIMARY KEY AUTO_INCREMENT, studentid VARCHAR(50) DEFAULT NULL, studentname VARCHAR(50) DEFAULT NULL, total_attendance INT DEFAULT NULL, date_added DATETIME DEFAULT CURRENT_TIMESTAMP);"
            cursor.execute(query)
            connection.commit()
#             connection.close()
            print(courseDept)
            query = f"INSERT INTO courses (coursecode, coursetitle, department, lecturer) VALUES ('{courseCode}', '{courseTitle}', '{courseDept}', '{courseLecturer}');"
            print(query)
            cursor.execute(query)
            connection.commit()
            connection.close()
            
            messagebox.showinfo("Response ", "Course added successfully.")
            return 0
        except pymysql.err.InternalError:
            connection.close()
            logging.exception('message')
            messagebox.showinfo("Response", "course: "+tablename+", already exists.")
            return 1
        except pymysql.err.ProgrammingError:
            logging.exception('message')
            connection.close()
            messagebox.showinfo("Response", "Please supply valid data")
            return 1
        else:
            connection.close()
            logging.exception('message')
            messagebox.showinfo("Response", "Error Adding Course")
            return 2