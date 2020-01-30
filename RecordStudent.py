from tkinter import *
from tkinter import messagebox
from PIL import Image
from tkinter import PhotoImage
import cv2
import os
import face_recognition
import logging
import time
import pymysql
class RecordStudent():
    def resizeImage(imgtoresize, imgtoresizename):
        openImage = Image.open(imgtoresize)
        newimg = openImage.resize((200, 200), Image.ANTIALIAS)
        newimg.save(imgtoresizename, "png")

    #start incrementattendance
    def incrementattendance(course_code, id_number, oldattendance):
        newatt = oldattendance+1
        connection = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")

        try:
            cursor = connection.cursor()
            query = f"UPDATE {course_code} SET total_attendance = {newatt} WHERE studentid = '{id_number}';"
            cursor.execute(query)

            connection.commit()
            connection.close()

            return 0
        except pymysql.err.InternalError:
            connection.close()
            messagebox.showinfo("Response", "code 1: Error updating attendance")
            return 1  # not used
        else:
            connection.close()
            messagebox.showinfo("Response", "code 2: Error  updating attendance ")
            return 2  # not used
    #end incrementattendance

    #start checkformatch
    def checkformatch(imagename):
        try:
            studentimage = face_recognition.load_image_file('./imgRecord.png')
            studentimage_encoding = face_recognition.face_encodings(studentimage)[0]

            image_to_compare = face_recognition.load_image_file(
                './students/'+imagename)
            image_to_compare_encoding = face_recognition.face_encodings(image_to_compare)[0]

            # Compare faces
            results = face_recognition.compare_faces(
                [studentimage_encoding], image_to_compare_encoding)

            if results[0]:
                return 1 #found image
            else:
                return 0
        except:
            logging.exception("message")
            print("couldnt compare "+imagename+", trained image might not contain a face")
            messagebox.showinfo("Response", "couldnt compare "+imagename+", trained image might not contain a face")
            return 0

    #end checkformatch

    #start checkifface
    def checkifface(filename):
        if os.path.exists(filename) == False:
            messagebox.showinfo("Response", "Image was not captured")
            return 1 #file doesnt exist
        image = face_recognition.load_image_file('./'+filename)
        face_locations = face_recognition.face_locations(image)
        # print(f'There are {len(face_locations)} people in this image')
        if len(face_locations) == 0:
            messagebox.showinfo("Response", "No face detected, please position your full face")
            return 2
        else:
            return 0
    #end checkifface

    #start getstudentsdetails
    def getstudentsdetails(coursecode):
        connection = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")

        try:
            cursor = connection.cursor()
            query = f"SELECT studentid, total_attendance, students.firstname, students.lastname, students.department, students.imagename FROM {coursecode} INNER JOIN students ON {coursecode}.studentid = students.idnumber;"
            cursor.execute(query)
            stList = list()
            count = 0
            data = cursor.fetchall()
            for d in data:
                stList.append(d)
                #print(data[count])
                count = count + 1
            connection.commit()
            connection.close()
            count = 0

            sList = []
            cnt = 0
            for each in stList:
                sList.append(stList[cnt])
                cnt = cnt + 1
            # print("Studentslist is ")
            # print(sList)

            return sList
        except pymysql.err.InternalError:
            connection.close()
            messagebox.showinfo("Response", "Error loading students")
            return 1  # not used
        else:
            connection.close()
            messagebox.showinfo("Response", "Error  loading students")
            return 2  # not used
    #end getstudentsdetails

    def capture(self, course_cod):
        coursec = course_cod
        found = 0
        foundstudent = []
        imgName = "imgRecord.png"
        image_type = "RECORD"

        try: 
            cam = cv2.VideoCapture(0)
            cnt = 0
            # cv2.namedWindow("Image Capture")
            while True:
                ret, frame = cam.read()
                #add button to frame
            #     rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.imshow(">>>>>>>>>>>>>> PLEASE FOCUS ON THE CAMERA (PRESS 'SPACEBAR' TO CANCEL RECORDING) <<<<<<<<<<<<<<<<", frame)
                if not ret:
                    break
                k = cv2.waitKey(1)
                cnt = cnt+1
                # print(cnt)
                if cnt == 50:
                    # img_name = "opencv_frame_{}.png".format(img_counter)
                    img_name = imgName
                    cv2.imwrite(img_name, frame)
                    print("{} written!".format(img_name))
                    #check if image contains a face
                    res = RecordStudent.checkifface(img_name)
                    if res == 1:
                        break;
                        cam.release()
                        cv2.destroyAllWindows()
                    if res == 2:
                        break;
                        cam.release()
                        cv2.destroyAllWindows()
                    if res == 0:
                        print("face detected")
                        #get id numbers of students offering the course
                        studentsdetails = RecordStudent.getstudentsdetails(coursec)
                        for st in studentsdetails:
                            print(st)
                            #for each student offering this course, check if the image matches
                            getres = RecordStudent.checkformatch("Resized"+st[5])
                            if getres == 0:
                                found = 0
                                continue
                            elif getres == 1:
                                found = 1
                                foundstudent = st
                                messagebox.showinfo("Response", "Dear "+st[2]+" "+st[3]+ ", Your Attendance Has been updated successfully.")
                                #increment student attendance for the course
                                RecordStudent.incrementattendance(coursec, st[0], st[1])
                                break
                        if found == 0:
                            messagebox.showinfo("Response", "A face was detected but not found, please ensure you are enrolled.")
                        break

                if k%256 == 32:
                    # SPACE pressed
                    break
            
            cam.release()
            cv2.destroyAllWindows()
            if found == 1:
                return foundstudent
            else:
                return []
        except:
            logging.exception("message")
            messagebox.showinfo("Error", "couldn't load camera, please check that a Camera is plugged.")
            cv2.destroyAllWindows()
            return []
# response = RecordStudent.getstudentsdetails("eee102")
# print("Response is")
# print(response[0][5])
# response = RecordStudent.capture()
# response = CaptureImage.resizeImage("ImgReg.png", "resizedImage.png")