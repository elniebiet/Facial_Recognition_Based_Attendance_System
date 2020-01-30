import pymysql
import logging
from tkinter import *

class EnrollStudent():
    def enrollStudent(self, connection, courseCode, idNumber, firstName, lastName):
#         connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
        fullName = firstName+" "+lastName
        try:
            cursor = connection.cursor()            
            
            query = f"INSERT INTO {courseCode} (studentid, studentname, total_attendance, date_added) VALUES ('{idNumber}', '{fullName}', 0, CURRENT_TIMESTAMP);"
            print(query)
            cursor.execute(query)
            connection.commit()
            connection.close()
            
            messagebox.showinfo("Response ", idNumber + " has been enrolled successfully.")
            return 0
        except pymysql.err.InternalError:
            connection.close()
            logging.exception("message")
            messagebox.showinfo("Response", "Error adding " + idNumber)
            return 1
        except pymysql.err.IntegrityError:
            connection.close()
            messagebox.showinfo("Response", idNumber + "is already enrolled for this course.")
            return 3
        except pymysql.err.ProgrammingError:
            connection.close()
            messagebox.showinfo("Response", "Error Adding " + idNumber)
            return 1
        else:
            connection.close()
            messagebox.showinfo("Response", "Error Adding " + idNumber )
            return 2
        
    def delistStudent(self, connection, courseCode, idNumber):
#         connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
        try:
            cursor = connection.cursor()            
            
            query = f"DELETE FROM {courseCode} WHERE studentid = '{idNumber}';"
            print(query)
            cursor.execute(query)
            connection.commit()
            connection.close()
            
            messagebox.showinfo("Response ", idNumber + " Removed successfully.")
            return 0
        except pymysql.err.InternalError:
            connection.close()
            messagebox.showinfo("Response", "Error Removing " + idNumber)
            return 1
        except pymysql.err.IntegrityError:
            connection.close()
            messagebox.showinfo("Response", idNumber + "is not enrolled in this course.")
            return 3
        except pymysql.err.ProgrammingError:
            connection.close()
            messagebox.showinfo("Response", "Error Removing " + idNumber)
            return 1
        else:
            connection.close()
            messagebox.showinfo("Response", "Error Removing " + idNumber )
            return 2