from tkinter import *
import tkinter as tk
import sys
import os
from tkinter import PhotoImage
from tkinter import messagebox
import pymysql
import AddCourse
import clViewStudent
import CaptureImage
import os.path
import cv2
from PIL import Image
import UploadStudent
import EnrollStudent
import EditStudent
import ViewCourse
from shutil import copy
from tkinter import simpledialog
import RecordStudent
import face_recognition
screens = []


def say(mes):
    messagebox.showinfo("Response",mes)
    return
def tell(head, mes):
    messagebox.showinfo(head, mes)
    return
def prompt(question):
    res = simpledialog.askstring("Confirm", question)
    if res == 'Y' or res == 'y' or res == 'Yes' or res == 'yes':
        return 1
    else:
        return 0
def getCourseDetails(courseCode):
    connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
    if courseCode == "select" or courseCode == "":
        say("No Course Selected")
        return
    course = ViewCourse.ViewCourse()
    det = course.getCourseDetails(connect, courseCode)
    return det
def getTotalStudents(courseCode):
    connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
    if courseCode == "select" or courseCode == "":
        say("No Course Selected")
        return
    course = ViewCourse.ViewCourse()
    num = course.getTotalStudents(connect, courseCode)
    return num
    
def removeStudent(idNumber, firstName):
    connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
    rmS = EditStudent.EditStudent()
    res = rmS.removeStudent(connect, idNumber)
    if res == 0:
        #success removing from db
        #delete images now
        fname = firstName.lower().capitalize()
        file1 = "students/"+fname+idNumber+".png"
        file2 = "students/"+"Resized"+file1
        try:
            if os.path.exists(file1):
                os.remove(file1)
            if os.path.exists(file2):
                os.remove(file2)
        except: 
            say("Error removing student: files couldn't be removed")
            return
        say("Student removed successfully")
        callHistoryScreen()
    else: 
        say("Error removing student")
        return
def freeAlpha(str):
    str = str.replace(' ', '')
    str = str.lower().capitalize()
    if str == '':
        return ''
    str = str.strip()
    if str.isalpha() == False:
        return '' 
    return str
def freeNumber(numStr):
    newStr = numStr.replace(' ', '')
    if newStr == '':
        return ''
    newStr = numStr.strip()
    if newStr.isdigit() == False:
        return ''
    return newStr
    
def updateStudent(firstName, lastName, idNumber, department, oldIdNumber):
    #check entries
    firstName = freeAlpha(firstName)
    lastName = freeAlpha(lastName)
    idNumber = freeNumber(idNumber)
    oldIdNumber = freeNumber(oldIdNumber)
    if firstName == '':
        tell("Response", "Please supply a valid first name")
        return
    if lastName == '': 
        tell("Response", "Please supply a valid last name")
        return
    if idNumber == '': 
        tell("Response", "Please supply a valid id number")
        return
    if oldIdNumber == '':
        tell("Response", "Please select an ID Number")
        return
#     print(firstName, lastName, idNumber, department, oldIdNumber)
    if idNumber != oldIdNumber: 
        #check if id number already exists
        connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
        edt = EditStudent.EditStudent()
        resp = edt.checkNewIdExists(connect, idNumber)
        if resp == 0: #id number doesnt exist
            tell("Response", "ID Number doesn't exist")
            return
    else:
        #update details
        connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
        updt = EditStudent.EditStudent()
        resp = updt.updateDetails(connect, idNumber, firstName, lastName)
        if resp == 0:
            tell("Response", "Record Updated Successfully")
            callHistoryScreen()
        else:
            tell("Response", "Error Updating "+idNumber)
            return
def setText(wid, text):
    wid.delete(1.0, "end-1c")
    wid.insert(END, text)
def getStudentsList(deptName):
    connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
    edt = EditStudent.EditStudent()
    resp = edt.getStudentsFromDept(connect,deptName)
    if resp == 1 or resp == 2:
        print("couldnt load students")
        return
    else:
        print(resp)
        return resp
def getImageName(id_number):
    connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
    viewst = clViewStudent.ViewStudent()
    imgname = viewst.getStudentImageName(connect, id_number)
    if imgname == '':
        tell("Response", "Error fetching Image Name")
        return ''
    else: 
        return imgname
def delistStudent(enCourseCode, enIDNumber):
    connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
    enl = EnrollStudent.EnrollStudent()
    resp = enl.delistStudent(connect, enCourseCode, enIDNumber)
    if resp == 0:
        print("Student successfully removed from this course")
        callHistoryScreen()
    else:
        print("Error delisting student")
def enrollStudent(enCourseCode, enIDNumber, enFirstName, enLastName):
    connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
    enl = EnrollStudent.EnrollStudent()
    resp = enl.enrollStudent(connect, enCourseCode, enIDNumber, enFirstName, enLastName)
    if resp == 0:
        print("Student enrolled successfully")
        callHistoryScreen()
    elif resp == 3: 
        print("Student already enrolled")
    else: 
        print("Student enroll failed")
        callHistoryScreen()
def captureRegImage():
    capt = CaptureImage.CaptureImage()
    resp = capt.capture("REG")
    if resp == 0:
        print("image captured") 
        callRegisterStudentsScreen()
        #create person and upload image
        #delete image
    else:
        tell("Response", "couldn't capture image")
def uploadStudent(fname, lname, dept, idNumber):
    fname = fname.strip()
    lname = lname.strip()
    if len(fname) < 2 or fname.isalpha() == False:
        tell("Response", "enter a valid first name")
        return
    if len(lname) < 2 or lname.isalpha() == False:
        tell("Response", "enter a valid last name")
        return
    if len(dept) == 0:
        tell("Response", "please select a department")
        return
    if len(idNumber) < 2 or idNumber.isdigit() == False:  #to implement - check if idnumber has no space
        tell("Response", "Please enter a valid ID Number, digits only")
        return
    if(os.path.exists("ImgReg.png") == False):
        tell("Response", "Please capture your face")
        return
    #upload student
    fname = fname.lower().capitalize()
    lname = lname.lower().capitalize()
    
    upl = UploadStudent.UploadStudent()
    connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
    resp = upl.upload(connect, idNumber, fname, lname, dept, fname+idNumber+".png")
    print(resp)
    if resp == 0:
        try:
            os.remove("ImgReg.png")
            os.remove("ResizedImgReg.png")
            callHistoryScreen()
#             callRegisterStudentsScreen()
        except:
            print("Error removing files")
    else: 
        return
    
#get dept courses
def getDeptCourses(courseDept):
    connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
    try:
        cursor = connect.cursor()
        query = f"SELECT coursecode FROM courses WHERE department = '{courseDept}';"
        cursor.execute(query)
        deptList = list()
        count = 0
        data = cursor.fetchall()
        for d in data:
            deptList.append(d[0])  
#             print(data[count])
            count = count+1    
        connect.commit()
        connect.close()
        count = 0
#         print(deptList)
        return deptList
    except:
        tell("Response", "couldn't get courses...")
        connect.close()
    

        
def getDepts():
    connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
    try:
        cursor = connect.cursor()
        query = f"SELECT name FROM departments;"
        cursor.execute(query)
        deptList = list()
        count = 0
        data = cursor.fetchall()
        for d in data:
            deptList.append(d[0])  
#             print(data[count])
            count = count+1    
        connect.commit()
        connect.close()
        count = 0
        return deptList
    except:
        tell("Response", "couldn't load departments ...")
        connect.close()
    
def addACourse(courseCode, courseTitle, courseDept, courseLecturer):
    if len(courseCode) < 3:
            tell("Response", "please enter a valid course code")
            return
    if len(courseTitle) < 3:
            tell("Response", "please enter a valid course title")
            return
    if len(courseDept) == 0:
            tell("Response", "please select a department")
            return
    if len(courseLecturer) < 2:
            tell("Response", "please enter a valid course lecturer name")
            return
    addC = AddCourse.AddCourse()
    connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
    res = addC.createTable(connect, courseCode, courseCode, courseTitle, courseDept, courseLecturer)
    #make directory for course
    os.mkdir("courses/"+courseCode.lower())
    callHistoryScreen()
#     if res == 0:
#         txtAddCourseCode.insert("END", "")
#         txtAddCourseTitle.insert("END", "")
#         txtAddCourseLecturer.insert("END", "")
        
def restart_app():
#     python = sys.executable
#     os.execl(python, python, * sys.argv)
    loginScreen.destroy()

def checkLogin(usr, pas):
    try:
        connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
        loginCursor = connect.cursor()
        query = f"SELECT * FROM admin WHERE username='{usr}' AND password='{pas}'"
        loginCursor.execute(query)
        connect.commit()
        if(loginCursor.rowcount == 0):
            tell("Response", "Please Enter valid login credentials")
            connect.close()
        else:
            connect.close()
            callHomeScreen()
    except:
        tell("Response", "Couldn't connect to database")
#
def closeScreen(screen):
    screen.withdraw()
def closeBackHome(screen):
    screen.withdraw()
    homeScreen.update()
    homeScreen.deiconify()
def refreshApp(screen):
    screen.update()
    screen.deiconify()
    
def center(tplevel):
    tplevel.update_idletasks()

    # Tkinter way to find the screen resolution
    screen_width = tplevel.winfo_screenwidth()
    screen_height = tplevel.winfo_screenheight()
    # PyQt way to find the screen resolution
#     app = QtGui.QApplication([])
#     screen_width = app.desktop().screenGeometry().width()
#     screen_height = app.desktop().screenGeometry().height()

    size = tuple(int(_) for _ in tplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2

    tplevel.geometry("+%d+%d" % (x, y))

def alignScreen(scr):
    scr.resizable(0,0)
    center(scr)

def withdrawAll(scr):
#     viewStudentScreen, viewCourseScreen, registerStudentScreen, recordAttendanceScreen, historyScreen,  editStudentScreen
#     screens = [addCourseScreen, homeScreen, loginScreen]
    for s in screens:
        if(s is not scr):
            s.withdraw()

def closeApp():
    loginScreen.destroy()

#
#
#
#
#
######Record Course Attendance Starts Here
def callRecordCourseAttendanceScreen():
    global EnrollStudentScreen
    global exitImage, refreshImage, addImage, recordImage, enrollImage, registerStudentsImage, viewStudentImage
    global editStudentImage, historyImage, viewCourseDetailsImage, resetImage

    EnrollStudentScreen = Toplevel(loginScreen)
    EnrollStudentScreen.geometry("1200x600")
    EnrollStudentScreen.title("")
    screens.append(EnrollStudentScreen)
    withdrawAll(EnrollStudentScreen)
    alignScreen(EnrollStudentScreen)
    EnrollStudentScreen.deiconify()
    c = Canvas(EnrollStudentScreen, bg="#9badcc", width="1200", height="600")
    c.place(x=0, y=0)
    lblFrameHeader = LabelFrame(EnrollStudentScreen, bg="#4285f4", text=" Home Screen ", font="10", fg="#fff")
    lblFrameHeader.pack(fill="both", expand="no")
    lblHeader = Label(lblFrameHeader, text="FACIAL RECOGNITION ATTENDANCE SYSTEM", width=100 \
                      , height="1", font=2, bg="#4285f4", fg="#fff")
    lblHeader.pack()

    exitImage = PhotoImage(file="icons/page_back.png")
    btnExit = tk.Button(lblFrameHeader, text="EXIT", width=50, fg="#fff", bg="#4285f4", \
                        relief=FLAT, image=exitImage, compound="left", command=lambda: closeApp())
    btnExit.place(x=0, y=0)

    refreshImage = PhotoImage(file="icons/page_refresh.png")
    btnRefresh = tk.Button(lblFrameHeader, text="Refresh", width=50, fg="#fff", bg="#4285f4", \
                           relief=FLAT, image=refreshImage, compound="left")
    btnRefresh.place(x=90, y=0)

    actionsFrame = Frame(EnrollStudentScreen, bg="#fff", height="550", width="300")
    actionsFrame.place(x=20, y=60)

    actionsHeader = LabelFrame(actionsFrame, bg="#d8dde6", text=" ACTIONS ", height="500", width="300" \
                               , fg="red", font="10")
    actionsHeader.pack(fill="both", expand="no")

    xAction = 5
    yAction = 10

    addImage = PhotoImage(file="icons/page_add.png")
    btnAddCourse = tk.Button(actionsHeader, text=" Add a Course", width="100", fg="red", relief=FLAT, image=addImage, \
                             compound="left", command=lambda: callAddCourseScreen())
    btnAddCourse.place(x=xAction, y=yAction)
    recordImage = PhotoImage(file="icons/page_save.png")
    btnRecord = tk.Button(actionsHeader, text=" Record Attendance", width="130", fg="red", relief=FLAT,
                          image=recordImage, \
                          compound="left", command=lambda: callRecordCourseAttendanceScreen())
    btnRecord.place(x=xAction, y=yAction + 30)
    enrollImage = PhotoImage(file="icons/page_white_put.png")
    btnEnroll = tk.Button(actionsHeader, text=" Enroll/Remove Students for a Course", width="230", fg="red",
                          relief=FLAT, image=enrollImage, \
                          compound="left", command=lambda: callEnrollStudentScreen())
    btnEnroll.place(x=xAction, y=yAction + 60)
    registerStudentsImage = PhotoImage(file="icons/page_attach.png")
    btnRegisterStudents = tk.Button(actionsHeader, text=" Register Students ", width="120", fg="red", relief=FLAT,
                                    image=registerStudentsImage, \
                                    compound="left", command=lambda: callRegisterStudentsScreen())
    btnRegisterStudents.place(x=xAction, y=yAction + 90)
    viewStudentImage = PhotoImage(file="icons/page_white_magnify.png")
    btnViewStudent = tk.Button(actionsHeader, text=" View Student ", width="100", fg="red", relief=FLAT,
                               image=viewStudentImage, \
                               compound="left", command=lambda: callViewStudentScreen())
    btnViewStudent.place(x=xAction, y=yAction + 120)
    editStudentImage = PhotoImage(file="icons/page_white_edit.png")
    btnEditStudent = tk.Button(actionsHeader, text=" Edit/Remove Student ", width="140", fg="red", relief=FLAT,
                               image=editStudentImage, \
                               compound="left", command=lambda: callEditStudentScreen())
    btnEditStudent.place(x=xAction, y=yAction + 150)
    viewCourseDetailsImage = PhotoImage(file="icons/page_white_find.png")
    btnViewCourseDetails = tk.Button(actionsHeader, text=" View Course Details ", width="135", fg="red", relief=FLAT,
                                     image=viewCourseDetailsImage, \
                                     compound="left", command=lambda: callViewCourseScreen())
    btnViewCourseDetails.place(x=xAction, y=yAction + 180)
    historyImage = PhotoImage(file="icons/folder.png")
    btnHistory = tk.Button(actionsHeader, text=" History", width="65", fg="red", relief=FLAT, image=historyImage, \
                           compound="left", command=lambda: callHistoryScreen())
    btnHistory.place(x=xAction, y=yAction + 210)
    resetImage = PhotoImage(file="icons/page_white_delete.png")
    btnReset = tk.Button(actionsHeader, text=" Reset App", width="80", fg="red", relief=FLAT, image=resetImage, \
                         compound="left")
    btnReset.place(x=xAction, y=yAction + 240)

    #####View Course Details
    ViewStudent = Frame(EnrollStudentScreen, bg="#9badcc", height="500", width="800")
    ViewStudent.place(x=350, y=60)

    ViewStudentHeader = LabelFrame(ViewStudent, text=" Record Student's Attendance ", font="8", bg="#9badcc", \
                                   height="500", width="800")
    ViewStudentHeader.pack(fill="both", expand="no")

    xViewStudent = 20
    yViewStudent = 30

    xViewCourse = 20
    yViewCourse = -65

    numAttendance = 0

    lblSelectStudentDept = Label(ViewStudentHeader, text="Department: ", font=5, fg="#fff", bg="#9badcc")
    lblSelectStudentDept.place(x=xViewStudent, y=yViewStudent - 25)

    viewStudentDeptList = getDepts()
    var4 = StringVar()
    deptCourses = []

    def changedVar4(*args):
        selectedDeptVar4 = var4.get()
        deptCourses = getDeptCourses(selectedDeptVar4)
        if len(deptCourses) == 0:
            viewStudentCourseList = ['select']
        else:
            viewStudentCourseList = deptCourses
        var5 = StringVar()

        def changedVar5(*args):
            selectedCourseVar5 = var5.get()
            courseName = selectedCourseVar5
            #             load course details
            courseDetails = getCourseDetails(courseName)
            if courseDetails == 1 or courseDetails == 2 or courseDetails == None:
                courseC = ''
                courseT = ''
                courseD = ''
                courseL = ''
            else:
                courseC = courseDetails[0][1].upper()
                courseT = courseDetails[0][2]
                courseD = courseDetails[0][3]
                courseL = courseDetails[0][4]

                lblViewCourseCode = Label(ViewStudentHeader, text="Course Code: ", font=5, fg="#000", bg="#fff",
                                          width="20")
                lblViewCourseCode.place(x=xViewCourse, y=yViewCourse + 110)
                lblViewCourseCodeValue = Label(ViewStudentHeader, text=courseC, font=5, fg="red", bg="#fff", width="20", anchor="w")
                lblViewCourseCodeValue.place(x=xViewCourse + 200, y=yViewCourse + 110)
                #
                lblViewCourseTitle = Label(ViewStudentHeader, text="Course Title: ", font=5, fg="#000", bg="#fff",
                                           width="20")
                lblViewCourseTitle.place(x=xViewCourse, y=yViewCourse + 140)
                lblViewCourseTitleValue = Label(ViewStudentHeader, text="", font=5, fg="red", bg="#fff", width="50", anchor="w")
                lblViewCourseTitleValue.config(text = courseT)
                lblViewCourseTitleValue.place(x=xViewCourse + 200, y=yViewCourse + 140)
                # lblViewCourseTitleValue.master.update()

                #
                lblViewDept = Label(ViewStudentHeader, text="Department: ", font=5, fg="#000", bg="#fff", width="20")
                lblViewDept.place(x=xViewCourse, y=yViewCourse + 170)
                lblViewDeptValue = Label(ViewStudentHeader, text=courseD, font=5, fg="red", bg="#fff", width="50", anchor="w")
                lblViewDeptValue.place(x=xViewCourse + 200, y=yViewCourse + 170)
                #
                lblViewLecturer = Label(ViewStudentHeader, text="Lecturer: ", font=5, fg="#000", bg="#fff", width="20")
                lblViewLecturer.place(x=xViewCourse, y=yViewCourse + 200)
                lblViewLecturerValue = Label(ViewStudentHeader, text=courseL, font=5, fg="red", bg="#fff", width="40", anchor="w")
                lblViewLecturerValue.place(x=xViewCourse + 200, y=yViewCourse + 200)

                totalS = getTotalStudents(courseC.lower())

                lblTotal = Label(ViewStudentHeader, text="Total Enrolled Students: ", font=5, fg="#000", bg="#fff",
                                 width="20")
                lblTotal.place(x=xViewCourse, y=yViewCourse + 230)
                lblTotalValue = Label(ViewStudentHeader, text=totalS, font=5, fg="red", bg="#fff", width="10", anchor="w")
                lblTotalValue.place(x=xViewCourse + 200, y=yViewCourse + 230)

                ##record attendance action button
                btnRecordNow = Button(ViewStudentHeader, text=" Click Here To Record ", width="40", fg="red", border=4, \
                                     compound="left", command=lambda: recordStudent(courseC.lower()))
                btnRecordNow.place(x=xViewCourse + 200, y=yViewCourse + 260)

                #recordStudent start
                def recordStudent(course_cod):
                    recs = RecordStudent.RecordStudent()
                    resp = recs.capture(course_cod)
                    img_file_name, i_n, f_n, l_n = '', '', '', ''  #image name, id number, first name, last name, total attendance
                    a_t = 0

                    if resp == []:
                        img_file_name = "BlankImage.png"
                        i_n, f_n, l_n = '', '', ''
                        a_t = 0
                    else:
                        img_file_name = "students/Resized"+resp[5]
                        i_n = resp[0]
                        f_n = resp[2]
                        l_n = resp[3]
                        a_t = resp[1]

                        ##record attendance action frame
                        MainActionFrame = LabelFrame(ViewStudentHeader, text=" Attendance Record Status ", font="8",
                                                     bg="yellow", \
                                                     height="240", width="780")
                        MainActionFrame.place(x=xViewCourse - 12, y=yViewCourse + 300)

                        imgfilename = PhotoImage(file=img_file_name)
                        loginScreen.imgfilename = imgfilename
                        cvFrame = Frame(MainActionFrame, bg="#9badcc", \
                                        height="200", width="200")
                        cvFrame.place(x=5, y=0)
                        cvImage = Canvas(cvFrame, height=200, width=200)
                        #     cvImage.place(x=xReg, y=yReg)
                        cvImage.pack(fill="both", expand=1)
                        cvImage.create_image(0, 0, anchor=NW, image=imgfilename)

                        xView = 220
                        yView = -70
                        idnumbervalue = i_n
                        firstnamevalue = f_n
                        lastnamevalue = l_n
                        totalattendancevalue = a_t+1

                        lblLastRecorded = Label(MainActionFrame, text="Last Recorded Attendance", font=5, fg="green", bg="yellow",
                                            width="40")
                        lblLastRecorded.place(x=xView+20, y=yView + 80)

                        lblIdNumber = Label(MainActionFrame, text="ID Number: ", font=5, fg="#000", bg="#fff",
                                            width="20")
                        lblIdNumber.place(x=xView, y=yView + 110)
                        lblIdNumberValue = Label(MainActionFrame, text=idnumbervalue, font=5, fg="red", bg="#fff",
                                                 width="30", anchor="w")
                        lblIdNumberValue.place(x=xView + 200, y=yView + 110)
                        #
                        lblFirstName = Label(MainActionFrame, text="First Name: ", font=5, fg="#000", bg="#fff",
                                             width="20")
                        lblFirstName.place(x=xView, y=yView + 140)
                        lblFirstNameValue = Label(MainActionFrame, text=firstnamevalue, font=5, fg="red", bg="#fff",
                                                  width="30", anchor="w")
                        lblFirstNameValue.place(x=xView + 200, y=yView + 140)
                        #
                        lblLastName = Label(MainActionFrame, text="Last Name: ", font=5, fg="#000", bg="#fff",
                                            width="20")
                        lblLastName.place(x=xView, y=yView + 170)
                        lblLastNameValue = Label(MainActionFrame, text=lastnamevalue, font=5, fg="red", bg="#fff",
                                                 width="30", anchor="w")
                        lblLastNameValue.place(x=xView + 200, y=yView + 170)
                        #
                        lblTotalAttendance = Label(MainActionFrame, text="Total Attendance: ", font=5, fg="#000",
                                                   bg="#fff", width="20")
                        lblTotalAttendance.place(x=xView, y=yView + 200)
                        lblTotalAttendanceValue = Label(MainActionFrame, text=totalattendancevalue, font=5, fg="red",
                                                        bg="#fff", width="10", anchor="w")
                        lblTotalAttendanceValue.place(x=xView + 200, y=yView + 200)
                #recordStudent end


        var5.trace('w', changedVar5)

        lblSelectStudentCourse = Label(ViewStudentHeader, text="Select Course: ", font=5, fg="#fff", bg="#9badcc")
        lblSelectStudentCourse.place(x=xViewStudent + 400, y=yViewStudent - 25)

        viewStudentCourseDrop = OptionMenu(ViewStudentHeader, var5, *viewStudentCourseList)
        viewStudentCourseDrop.config(width=20)
        viewStudentCourseDrop.place(x=xViewStudent + 510, y=yViewStudent - 25)

    var4.trace('w', changedVar4)

    viewStudentDeptDrop = OptionMenu(ViewStudentHeader, var4, *viewStudentDeptList)
    viewStudentDeptDrop.config(width=30)
    viewStudentDeptDrop.place(x=xViewStudent + 100, y=yViewStudent - 25)


######Record Course Attendance Ends Here
#
#
#
#
#

#
#
#
#Enroll Students screen start     
def callEnrollStudentScreen():
    global EnrollStudentScreen
    global exitImage, refreshImage, addImage, recordImage, enrollImage, registerStudentsImage, viewStudentImage
    global editStudentImage, historyImage, viewCourseDetailsImage, resetImage

    EnrollStudentScreen = Toplevel(loginScreen)
    EnrollStudentScreen.geometry("1200x600")
    EnrollStudentScreen.title("")
    screens.append(EnrollStudentScreen)
    withdrawAll(EnrollStudentScreen)
    alignScreen(EnrollStudentScreen)
    EnrollStudentScreen.deiconify()
    c = Canvas(EnrollStudentScreen, bg="#9badcc", width="1200", height="600")
    c.place(x=0, y=0)
    lblFrameHeader = LabelFrame(EnrollStudentScreen, bg="#4285f4", text=" Home Screen ", font="10", fg="#fff")
    lblFrameHeader.pack(fill="both", expand="no")
    lblHeader = Label(lblFrameHeader, text = "FACIAL RECOGNITION ATTENDANCE SYSTEM", width=100 \
                      , height="1", font=2, bg="#4285f4", fg="#fff")
    lblHeader.pack()
     
    exitImage = PhotoImage(file="icons/page_back.png")
    btnExit = tk.Button(lblFrameHeader, text="EXIT", width=50, fg="#fff", bg="#4285f4", \
                 relief=FLAT, image=exitImage, compound="left", command=lambda: closeApp())
    btnExit.place(x=0, y=0)
     
    refreshImage = PhotoImage(file="icons/page_refresh.png")
    btnRefresh = tk.Button(lblFrameHeader, text="Refresh", width=50, fg="#fff", bg="#4285f4", \
                 relief=FLAT, image=refreshImage, compound="left")
    btnRefresh.place(x=90, y=0)
     
    actionsFrame = Frame(EnrollStudentScreen, bg="#fff", height="550", width="300")
    actionsFrame.place(x=20, y=60)
     
    actionsHeader = LabelFrame(actionsFrame, bg="#d8dde6", text=" ACTIONS ", height="500", width="300"\
                            ,fg="red", font="10")
    actionsHeader.pack(fill="both", expand="no")
     
    xAction = 5
    yAction = 10
     
    addImage = PhotoImage(file="icons/page_add.png")
    btnAddCourse = tk.Button(actionsHeader, text=" Add a Course", width="100", fg="red", relief=FLAT, image=addImage, \
                             compound="left", command=lambda: callAddCourseScreen())
    btnAddCourse.place(x=xAction, y=yAction)
    recordImage = PhotoImage(file="icons/page_save.png")
    btnRecord = tk.Button(actionsHeader, text=" Record Attendance", width="130", fg="red", relief=FLAT, image=recordImage, \
                          compound="left", command=lambda: callRecordCourseAttendanceScreen())
    btnRecord.place(x=xAction, y=yAction+30)
    enrollImage = PhotoImage(file="icons/page_white_put.png")
    btnEnroll= tk.Button(actionsHeader, text=" Enroll/Remove Students for a Course", width="230", fg="red", relief=FLAT, image=enrollImage, \
                             compound="left", command=lambda:callEnrollStudentScreen())
    btnEnroll.place(x=xAction, y=yAction+60)
    registerStudentsImage = PhotoImage(file="icons/page_attach.png")
    btnRegisterStudents= tk.Button(actionsHeader, text=" Register Students ", width="120", fg="red", relief=FLAT, image=registerStudentsImage, \
                             compound="left", command=lambda:callRegisterStudentsScreen())
    btnRegisterStudents.place(x=xAction, y=yAction+90)
    viewStudentImage = PhotoImage(file="icons/page_white_magnify.png")
    btnViewStudent = tk.Button(actionsHeader, text=" View Student ", width="100", fg="red", relief=FLAT, image=viewStudentImage, \
                             compound="left", command=lambda:callViewStudentScreen())
    btnViewStudent.place(x=xAction, y=yAction+120)
    editStudentImage = PhotoImage(file="icons/page_white_edit.png")
    btnEditStudent = tk.Button(actionsHeader, text=" Edit/Remove Student ", width="140", fg="red", relief=FLAT, image=editStudentImage, \
                             compound="left", command=lambda: callEditStudentScreen())
    btnEditStudent.place(x=xAction, y=yAction+150)
    viewCourseDetailsImage = PhotoImage(file="icons/page_white_find.png")
    btnViewCourseDetails = tk.Button(actionsHeader, text=" View Course Details ", width="135", fg="red", relief=FLAT, image=viewCourseDetailsImage, \
                             compound="left", command=lambda:callViewCourseScreen())
    btnViewCourseDetails.place(x=xAction, y=yAction+180)
    historyImage = PhotoImage(file="icons/folder.png")
    btnHistory = tk.Button(actionsHeader, text=" History", width="65", fg="red", relief=FLAT, image=historyImage, \
                             compound="left", command=lambda: callHistoryScreen())
    btnHistory.place(x=xAction, y=yAction+210) 
    resetImage = PhotoImage(file="icons/page_white_delete.png")
    btnReset = tk.Button(actionsHeader, text=" Reset App", width="80", fg="red", relief=FLAT, image=resetImage, \
                             compound="left")
    btnReset.place(x=xAction, y=yAction+240) 
     
     
     
    #####Enroll a Student
    ViewStudent= Frame(EnrollStudentScreen, bg="#9badcc", height="500", width="800")
    ViewStudent.place(x=350, y=60)
         
    ViewStudentHeader = LabelFrame(ViewStudent, text=" Enroll Student For Course / Delist Student ", font="8", bg="#9badcc", \
                                   height="500", width="800")
    ViewStudentHeader.pack(fill="both", expand="no")
        
    xViewStudent= 20
    yViewStudent = 30
    numAttendance = 0
        
    lblSelectStudentDept = Label(ViewStudentHeader, text="Select Department: ", font=5, fg="#fff", bg="#9badcc")
    lblSelectStudentDept.place(x=xViewStudent, y=yViewStudent)
    
    
    viewStudentDeptList = getDepts()
    var4 = StringVar()
    deptCourses = []
    def changedVar4(*args):
        selectedDeptVar4 = var4.get()
        deptCourses = getDeptCourses(selectedDeptVar4)
        if len(deptCourses) == 0:
            viewStudentCourseList = ['select']
        else:
            viewStudentCourseList = deptCourses
            lblSelectStudentName = Label(ViewStudentHeader, text="Select Student: ", font=5, fg="#fff", bg="#9badcc")
            lblSelectStudentName.place(x=xViewStudent, y=yViewStudent+100)
        var5 = StringVar()
        def changedVar5(*args):
            selectedCourseVar5 = var5.get()
            courseName = selectedCourseVar5
#             load id numbers
            getStudents = clViewStudent.ViewStudent
            connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
            stList = getStudents.getStudentsFromDept(connect, selectedDeptVar4)
            viewStudentNameList = []
            if stList == None:
                viewStudentNameList = ['select']
            else:
                count = 0
                nameList = []
                for each in stList:
                    nameList.append(stList[count][0])
                    count = count+1
                print(nameList)
                viewStudentNameList = nameList

#             selectedCourseStudents = getSelectedCourseStudents(selectedDeptVar4)
            

            var6 = StringVar()
            def changedVar6(*args):
                selectedStudentVar6 = var6.get()
#                 print(selectedStudentVar6)
#                 print(selectedCourseVar5)
#                 get student details
                getDet = clViewStudent.ViewStudent()
                con = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
#                 print(selectedStudentVar6)
                stDet = getDet.getStudentDetailsFromDept(con, selectedCourseVar5, selectedStudentVar6)
                stIDNumber = selectedStudentVar6
                print("Student details")
                print(stDet)
                stFirstName = StringVar()
                stLastName = StringVar()
                stImageName = StringVar()
                if len(stList) == 0:
                    stFirstName = ''
                    stLastName = ''
                    stImageName = 'BlankImage.png'
                else:
                    stFirstName = stDet[0][0]
                    stLastName = stDet[0][1]
                    stImageName = 'students/Resized'+stDet[0][2]
                    print(stFirstName)
                    lblStudentName = Label(ViewStudentHeader, text="Student Name: ", font="1")
                    lblStudentName.place(x=xViewStudent, y=yViewStudent+170)
                      
                    lblStudentNameValue = Label(ViewStudentHeader, text=stFirstName+" "+stLastName, font="1", fg="red", width=40)
                    lblStudentNameValue.place(x=xViewStudent+130, y=yViewStudent+170) 
                    enrollImgFileName = PhotoImage(file = "students/Resized"+stDet[0][2])  
                    loginScreen.enrollImgFileName = enrollImgFileName
                    #display Image
                    cvFrame = Frame(ViewStudentHeader, bg="#9badcc", \
                           height="200", width="200")
                    cvFrame.place(x=xViewStudent+170, y=yViewStudent+205)  
                    cvImage = Canvas(cvFrame, height=200, width=200) 
                    cvImage.pack(fill="both", expand=1)
                    cvImage.create_image(0, 0, anchor=NW, image=enrollImgFileName)

                btnEnroll = Button(ViewStudentHeader, text=" Enroll Student", width="20", fg="red", \
                             compound="left", command=lambda: enrollStudent(selectedCourseVar5, stIDNumber, stFirstName, stLastName))
                btnEnroll.place(x=xViewStudent + 100, y=yViewStudent+420)
                
                btnDelist = Button(ViewStudentHeader, text=" Delist Student", width="20", fg="red", \
                             compound="left", command=lambda: delistStudent(selectedCourseVar5, stIDNumber))
                btnDelist.place(x=xViewStudent + 320, y=yViewStudent+420) 
#                 lblStudentName = Label(ViewStudentHeader, text="Student Name: ", font="1")
#                 lblStudentName.place(x=xViewStudent, y=yViewStudent+170)
#                  
#                 lblStudentNameValue = Label(ViewStudentHeader, text=stName, font="1", fg="red", width=40)
#                 lblStudentNameValue.place(x=xViewStudent+130, y=yViewStudent+170) 
#                 
#                 lblNumAttendance = Label(ViewStudentHeader, text="Total Attendance: ", font="1")
#                 lblNumAttendance.place(x=xViewStudent, y=yViewStudent+210)
#                  
#                 lblNumAttendanceValue = Label(ViewStudentHeader, text=stAtt, font="1", fg="red", width=10)
#                 lblNumAttendanceValue.place(x=xViewStudent+150, y=yViewStudent+210) 

            
            var6.trace('w', changedVar6)
            try: 
                viewStudentNameDrop = OptionMenu(ViewStudentHeader,var6,*viewStudentNameList)
                viewStudentNameDrop.config(width=20)
                viewStudentNameDrop.place(x=xViewStudent+150, y=yViewStudent+100)
            except: 
                tell("Response", "Please make a selection")
             
            
        var5.trace('w', changedVar5)
        
        lblSelectStudentCourse = Label(ViewStudentHeader, text="Select Course: ", font=5, fg="#fff", bg="#9badcc")
        lblSelectStudentCourse.place(x=xViewStudent, y=yViewStudent+50)
        
        viewStudentCourseDrop = OptionMenu(ViewStudentHeader,var5,*viewStudentCourseList)
        viewStudentCourseDrop.config(width=20)
        viewStudentCourseDrop.place(x=xViewStudent+150, y=yViewStudent+50)
    
    var4.trace('w', changedVar4)
    
    viewStudentDeptDrop = OptionMenu(ViewStudentHeader,var4,*viewStudentDeptList)
    viewStudentDeptDrop.config(width=30)
    viewStudentDeptDrop.place(x=xViewStudent+150, y=yViewStudent)
      
    
    
#Enroll Students screen ends
#
#
#
def callViewStudentScreen():
    global viewStudentScreen
    global exitImage, refreshImage, addImage, recordImage, enrollImage, registerStudentsImage, viewStudentImage
    global editStudentImage, historyImage, viewCourseDetailsImage, resetImage

    viewStudentScreen = Toplevel(loginScreen)
    viewStudentScreen.geometry("1200x600")
    viewStudentScreen.title("")
    screens.append(viewStudentScreen)
    withdrawAll(viewStudentScreen)
    alignScreen(viewStudentScreen)
    viewStudentScreen.deiconify()
    c = Canvas(viewStudentScreen, bg="#9badcc", width="1200", height="600")
    c.place(x=0, y=0)
    lblFrameHeader = LabelFrame(viewStudentScreen, bg="#4285f4", text=" Home Screen ", font="10", fg="#fff")
    lblFrameHeader.pack(fill="both", expand="no")
    lblHeader = Label(lblFrameHeader, text = "FACIAL RECOGNITION ATTENDANCE SYSTEM", width=100 \
                      , height="1", font=2, bg="#4285f4", fg="#fff")
    lblHeader.pack()
     
    exitImage = PhotoImage(file="icons/page_back.png")
    btnExit = tk.Button(lblFrameHeader, text="EXIT", width=50, fg="#fff", bg="#4285f4", \
                 relief=FLAT, image=exitImage, compound="left", command=lambda: closeApp())
    btnExit.place(x=0, y=0)
     
    refreshImage = PhotoImage(file="icons/page_refresh.png")
    btnRefresh = tk.Button(lblFrameHeader, text="Refresh", width=50, fg="#fff", bg="#4285f4", \
                 relief=FLAT, image=refreshImage, compound="left")
    btnRefresh.place(x=90, y=0)
     
    actionsFrame = Frame(viewStudentScreen, bg="#fff", height="550", width="300")
    actionsFrame.place(x=20, y=60)
     
    actionsHeader = LabelFrame(actionsFrame, bg="#d8dde6", text=" ACTIONS ", height="500", width="300"\
                            ,fg="red", font="10")
    actionsHeader.pack(fill="both", expand="no")
     
    xAction = 5
    yAction = 10
     
    addImage = PhotoImage(file="icons/page_add.png")
    btnAddCourse = tk.Button(actionsHeader, text=" Add a Course", width="100", fg="red", relief=FLAT, image=addImage, \
                             compound="left", command=lambda: callAddCourseScreen())
    btnAddCourse.place(x=xAction, y=yAction)
    recordImage = PhotoImage(file="icons/page_save.png")
    btnRecord = tk.Button(actionsHeader, text=" Record Attendance", width="130", fg="red", relief=FLAT, image=recordImage, \
                          compound="left", command=lambda: callRecordCourseAttendanceScreen())
    btnRecord.place(x=xAction, y=yAction+30)
    enrollImage = PhotoImage(file="icons/page_white_put.png")
    btnEnroll= tk.Button(actionsHeader, text=" Enroll/Remove Students for a Course", width="230", fg="red", relief=FLAT, image=enrollImage, \
                             compound="left", command=lambda:callEnrollStudentScreen())
    btnEnroll.place(x=xAction, y=yAction+60)
    registerStudentsImage = PhotoImage(file="icons/page_attach.png")
    btnRegisterStudents= tk.Button(actionsHeader, text=" Register Students ", width="120", fg="red", relief=FLAT, image=registerStudentsImage, \
                             compound="left", command=lambda:callRegisterStudentsScreen())
    btnRegisterStudents.place(x=xAction, y=yAction+90)
    viewStudentImage = PhotoImage(file="icons/page_white_magnify.png")
    btnViewStudent = tk.Button(actionsHeader, text=" View Student ", width="100", fg="red", relief=FLAT, image=viewStudentImage, \
                             compound="left", command=lambda:callViewStudentScreen())
    btnViewStudent.place(x=xAction, y=yAction+120)
    editStudentImage = PhotoImage(file="icons/page_white_edit.png")
    btnEditStudent = tk.Button(actionsHeader, text=" Edit/Remove Student ", width="140", fg="red", relief=FLAT, image=editStudentImage, \
                             compound="left", command=lambda: callEditStudentScreen())
    btnEditStudent.place(x=xAction, y=yAction+150)
    viewCourseDetailsImage = PhotoImage(file="icons/page_white_find.png")
    btnViewCourseDetails = tk.Button(actionsHeader, text=" View Course Details ", width="135", fg="red", relief=FLAT, image=viewCourseDetailsImage, \
                             compound="left", command=lambda:callViewCourseScreen())
    btnViewCourseDetails.place(x=xAction, y=yAction+180)
    historyImage = PhotoImage(file="icons/folder.png")
    btnHistory = tk.Button(actionsHeader, text=" History", width="65", fg="red", relief=FLAT, image=historyImage, \
                             compound="left", command=lambda: callHistoryScreen())
    btnHistory.place(x=xAction, y=yAction+210) 
    resetImage = PhotoImage(file="icons/page_white_delete.png")
    btnReset = tk.Button(actionsHeader, text=" Reset App", width="80", fg="red", relief=FLAT, image=resetImage, \
                             compound="left")
    btnReset.place(x=xAction, y=yAction+240) 
     
     
     
    #####View a Student
    ViewStudent= Frame(viewStudentScreen, bg="#9badcc", height="500", width="800")
    ViewStudent.place(x=350, y=60)
         
    ViewStudentHeader = LabelFrame(ViewStudent, text=" View Student Details ", font="8", bg="#9badcc", \
                                   height="500", width="800")
    ViewStudentHeader.pack(fill="both", expand="no")
        
    xViewStudent= 20
    yViewStudent = 30
    numAttendance = 0
        
    lblSelectStudentDept = Label(ViewStudentHeader, text="Select Department: ", font=5, fg="#fff", bg="#9badcc")
    lblSelectStudentDept.place(x=xViewStudent, y=yViewStudent)
    
    
    viewStudentDeptList = getDepts()
    var4 = StringVar()
    deptCourses = []
    def changedVar4(*args):
        selectedDeptVar4 = var4.get()
        deptCourses = getDeptCourses(selectedDeptVar4)
        if len(deptCourses) == 0:
            viewStudentCourseList = ['select']
        else:
            viewStudentCourseList = deptCourses
        var5 = StringVar()
        def changedVar5(*args):
            selectedCourseVar5 = var5.get()
            courseName = selectedCourseVar5
#             load id numbers
            getStudents = clViewStudent.ViewStudent
            connect = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
            stList = getStudents.getStudents(connect, courseName)
            print(stList)
            viewStudentNameList = []
            if stList == None:
                viewStudentNameList = ['select']
            else:
                count = 0
                nameList = []
                for each in stList:
                    nameList.append(stList[count][0])
                    count = count+1
                print(nameList)
                viewStudentNameList = nameList

#             selectedCourseStudents = getSelectedCourseStudents(selectedDeptVar4)
            lblSelectStudentName = Label(ViewStudentHeader, text="Select Student: ", font=5, fg="#fff", bg="#9badcc")
            lblSelectStudentName.place(x=xViewStudent, y=yViewStudent+100)
            

            var6 = StringVar()
            def changedVar6(*args):
                selectedStudentVar6 = var6.get()
                print(selectedStudentVar6)
                print(selectedCourseVar5)
#                 get student details
                getDet = clViewStudent.ViewStudent()
                con = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
                stDet = getDet.getStudentDetails(con, selectedCourseVar5, selectedStudentVar6)
                stAtt = StringVar()
                if stList == None:
                    stAtt = ''
                    stName = ''
                else:
                    stAtt = stDet[0][1]
                    stName = stDet[0][0]
                
                #display Image here
                studentImageName = getImageName(selectedStudentVar6)
                if os.path.exists("students/Resized"+studentImageName) == False:
                    viewImgFileName = PhotoImage(file = "BlankImage.png")                      
                else:
                    viewImgFileName = PhotoImage(file = "students/Resized"+studentImageName)  
                loginScreen.viewImgFileName = viewImgFileName
                cvFrame = Frame(ViewStudentHeader, bg="#9badcc", height="200", width="200")
                cvFrame.place(x=xViewStudent+170, y=yViewStudent+150)  
                cvImage = Canvas(cvFrame, height=200, width=200) 
                cvImage.pack(fill="both", expand=1)
                cvImage.create_image(0, 0, anchor=NW, image=viewImgFileName)


                lblStudentName = Label(ViewStudentHeader, text="Student Name: ", font="1")
                lblStudentName.place(x=xViewStudent, y=yViewStudent+370)
                 
                lblStudentNameValue = Label(ViewStudentHeader, text=stName, font="1", fg="red", width=40)
                lblStudentNameValue.place(x=xViewStudent+130, y=yViewStudent+370) 
                
                lblNumAttendance = Label(ViewStudentHeader, text="Total Attendance: ", font="1")
                lblNumAttendance.place(x=xViewStudent, y=yViewStudent+410)
                 
                lblNumAttendanceValue = Label(ViewStudentHeader, text=stAtt, font="1", fg="red", width=10)
                lblNumAttendanceValue.place(x=xViewStudent+150, y=yViewStudent+410) 

            
            var6.trace('w', changedVar6)
            
            viewStudentNameDrop = OptionMenu(ViewStudentHeader,var6,*viewStudentNameList)
            viewStudentNameDrop.config(width=20)
            viewStudentNameDrop.place(x=xViewStudent+150, y=yViewStudent+100)
            
             
            
        var5.trace('w', changedVar5)
        
        lblSelectStudentCourse = Label(ViewStudentHeader, text="Select Course: ", font=5, fg="#fff", bg="#9badcc")
        lblSelectStudentCourse.place(x=xViewStudent, y=yViewStudent+50)
    
        viewStudentCourseDrop = OptionMenu(ViewStudentHeader,var5,*viewStudentCourseList)
        viewStudentCourseDrop.config(width=20)
        viewStudentCourseDrop.place(x=xViewStudent+150, y=yViewStudent+50)
    
    var4.trace('w', changedVar4)
    
    viewStudentDeptDrop = OptionMenu(ViewStudentHeader,var4,*viewStudentDeptList)
    viewStudentDeptDrop.config(width=30)
    viewStudentDeptDrop.place(x=xViewStudent+150, y=yViewStudent)
      
    
#     if len(deptCourses) == 0 :
#         viewStudentCourseList = ["select"]
#         print(deptCourses)
#     else :
#         print(deptCourses)
    

    ####View a Student Details
# 
def callViewCourseScreen():
    global EnrollStudentScreen
    global exitImage, refreshImage, addImage, recordImage, enrollImage, registerStudentsImage, viewStudentImage
    global editStudentImage, historyImage, viewCourseDetailsImage, resetImage

    EnrollStudentScreen = Toplevel(loginScreen)
    EnrollStudentScreen.geometry("1200x600")
    EnrollStudentScreen.title("")
    screens.append(EnrollStudentScreen)
    withdrawAll(EnrollStudentScreen)
    alignScreen(EnrollStudentScreen)
    EnrollStudentScreen.deiconify()
    c = Canvas(EnrollStudentScreen, bg="#9badcc", width="1200", height="600")
    c.place(x=0, y=0)
    lblFrameHeader = LabelFrame(EnrollStudentScreen, bg="#4285f4", text=" Home Screen ", font="10", fg="#fff")
    lblFrameHeader.pack(fill="both", expand="no")
    lblHeader = Label(lblFrameHeader, text = "FACIAL RECOGNITION ATTENDANCE SYSTEM", width=100 \
                      , height="1", font=2, bg="#4285f4", fg="#fff")
    lblHeader.pack()
     
    exitImage = PhotoImage(file="icons/page_back.png")
    btnExit = tk.Button(lblFrameHeader, text="EXIT", width=50, fg="#fff", bg="#4285f4", \
                 relief=FLAT, image=exitImage, compound="left", command=lambda: closeApp())
    btnExit.place(x=0, y=0)
     
    refreshImage = PhotoImage(file="icons/page_refresh.png")
    btnRefresh = tk.Button(lblFrameHeader, text="Refresh", width=50, fg="#fff", bg="#4285f4", \
                 relief=FLAT, image=refreshImage, compound="left")
    btnRefresh.place(x=90, y=0)
     
    actionsFrame = Frame(EnrollStudentScreen, bg="#fff", height="550", width="300")
    actionsFrame.place(x=20, y=60)
     
    actionsHeader = LabelFrame(actionsFrame, bg="#d8dde6", text=" ACTIONS ", height="500", width="300"\
                            ,fg="red", font="10")
    actionsHeader.pack(fill="both", expand="no")
     
    xAction = 5
    yAction = 10
     
    addImage = PhotoImage(file="icons/page_add.png")
    btnAddCourse = tk.Button(actionsHeader, text=" Add a Course", width="100", fg="red", relief=FLAT, image=addImage, \
                             compound="left", command=lambda: callAddCourseScreen())
    btnAddCourse.place(x=xAction, y=yAction)
    recordImage = PhotoImage(file="icons/page_save.png")
    btnRecord = tk.Button(actionsHeader, text=" Record Attendance", width="130", fg="red", relief=FLAT, image=recordImage, \
                          compound="left", command=lambda: callRecordCourseAttendanceScreen())
    btnRecord.place(x=xAction, y=yAction+30)
    enrollImage = PhotoImage(file="icons/page_white_put.png")
    btnEnroll= tk.Button(actionsHeader, text=" Enroll/Remove Students for a Course", width="230", fg="red", relief=FLAT, image=enrollImage, \
                             compound="left", command=lambda:callEnrollStudentScreen())
    btnEnroll.place(x=xAction, y=yAction+60)
    registerStudentsImage = PhotoImage(file="icons/page_attach.png")
    btnRegisterStudents= tk.Button(actionsHeader, text=" Register Students ", width="120", fg="red", relief=FLAT, image=registerStudentsImage, \
                             compound="left", command=lambda:callRegisterStudentsScreen())
    btnRegisterStudents.place(x=xAction, y=yAction+90)
    viewStudentImage = PhotoImage(file="icons/page_white_magnify.png")
    btnViewStudent = tk.Button(actionsHeader, text=" View Student ", width="100", fg="red", relief=FLAT, image=viewStudentImage, \
                             compound="left", command=lambda:callViewStudentScreen())
    btnViewStudent.place(x=xAction, y=yAction+120)
    editStudentImage = PhotoImage(file="icons/page_white_edit.png")
    btnEditStudent = tk.Button(actionsHeader, text=" Edit/Remove Student ", width="140", fg="red", relief=FLAT, image=editStudentImage, \
                             compound="left", command=lambda: callEditStudentScreen())
    btnEditStudent.place(x=xAction, y=yAction+150)
    viewCourseDetailsImage = PhotoImage(file="icons/page_white_find.png")
    btnViewCourseDetails = tk.Button(actionsHeader, text=" View Course Details ", width="135", fg="red", relief=FLAT, image=viewCourseDetailsImage, \
                             compound="left", command=lambda:callViewCourseScreen())
    btnViewCourseDetails.place(x=xAction, y=yAction+180)
    historyImage = PhotoImage(file="icons/folder.png")
    btnHistory = tk.Button(actionsHeader, text=" History", width="65", fg="red", relief=FLAT, image=historyImage, \
                             compound="left", command=lambda: callHistoryScreen())
    btnHistory.place(x=xAction, y=yAction+210) 
    resetImage = PhotoImage(file="icons/page_white_delete.png")
    btnReset = tk.Button(actionsHeader, text=" Reset App", width="80", fg="red", relief=FLAT, image=resetImage, \
                             compound="left")
    btnReset.place(x=xAction, y=yAction+240) 
     
     
     
    #####View Course Details
    ViewStudent= Frame(EnrollStudentScreen, bg="#9badcc", height="500", width="800")
    ViewStudent.place(x=350, y=60)
         
    ViewStudentHeader = LabelFrame(ViewStudent, text=" View Course Details ", font="8", bg="#9badcc", \
                                   height="500", width="800")
    ViewStudentHeader.pack(fill="both", expand="no")
        
    xViewStudent= 20
    yViewStudent = 30
    
    xViewCourse = 20
    yViewCourse = 30
    
    numAttendance = 0
        
    lblSelectStudentDept = Label(ViewStudentHeader, text="Select Department: ", font=5, fg="#fff", bg="#9badcc")
    lblSelectStudentDept.place(x=xViewStudent, y=yViewStudent)
    
    
    viewStudentDeptList = getDepts()
    var4 = StringVar()
    deptCourses = []
    def changedVar4(*args):
        selectedDeptVar4 = var4.get()
        deptCourses = getDeptCourses(selectedDeptVar4)
        if len(deptCourses) == 0:
            viewStudentCourseList = ['select']
        else:
            viewStudentCourseList = deptCourses
        var5 = StringVar()
        def changedVar5(*args):
            selectedCourseVar5 = var5.get()
            courseName = selectedCourseVar5
#             load course details
            courseDetails = getCourseDetails(courseName)
            if courseDetails == 1 or courseDetails == 2 or courseDetails == None:
                courseC = ''
                courseT = ''
                courseD = ''
                courseL = ''
            else: 
                courseC = courseDetails[0][1].upper()
                courseT = courseDetails[0][2]
                courseD = courseDetails[0][3]
                courseL = courseDetails[0][4]
                
                lblViewCourseCode = Label(ViewStudentHeader, text="Course Code: ", font=5, fg="#000", bg="#fff", width="20")
                lblViewCourseCode.place(x=xViewCourse, y=yViewCourse+110)
                lblViewCourseCodeValue= Label(ViewStudentHeader, text=courseC, font=5, fg="red", bg="#fff", width="20", anchor="w")
                lblViewCourseCodeValue.place(x=xViewCourse+200,y=yViewCourse+110)
#                        
                lblViewCourseTitle = Label(ViewStudentHeader, text="Course Title: ", font=5, fg="#000", bg="#fff", width="20")
                lblViewCourseTitle.place(x=xViewCourse, y=yViewCourse+140)
                lblViewCourseTitleValue= Label(ViewStudentHeader, text=courseT, font=5, fg="red", bg="#fff", width="50", anchor="w")
                lblViewCourseTitleValue.place(x=xViewCourse+200,y=yViewCourse+140)
#                        
                lblViewDept = Label(ViewStudentHeader, text="Department: ", font=5, fg="#000", bg="#fff", width="20")
                lblViewDept.place(x=xViewCourse, y=yViewCourse+170)
                lblViewDeptValue= Label(ViewStudentHeader, text=courseD, font=5, fg="red", bg="#fff", width="50", anchor="w")
                lblViewDeptValue.place(x=xViewCourse+200,y=yViewCourse+170)
#                        
                lblViewLecturer = Label(ViewStudentHeader, text="Lecturer: ", font=5, fg="#000", bg="#fff", width="20")
                lblViewLecturer.place(x=xViewCourse, y=yViewCourse+200)
                lblViewLecturerValue= Label(ViewStudentHeader, text=courseL, font=5, fg="red", bg="#fff", width="50", anchor="w")
                lblViewLecturerValue.place(x=xViewCourse+200,y=yViewCourse+200)
                
                totalS = getTotalStudents(courseC.lower())
                
                lblTotal = Label(ViewStudentHeader, text="Total Enrolled Students: ", font=5, fg="#000", bg="#fff", width="20")
                lblTotal.place(x=xViewCourse, y=yViewCourse+230)
                lblTotalValue= Label(ViewStudentHeader, text=totalS, font=5, fg="red", bg="#fff", width="10", anchor="w")
                lblTotalValue.place(x=xViewCourse+200,y=yViewCourse+230)
            
        var5.trace('w', changedVar5)
        
        lblSelectStudentCourse = Label(ViewStudentHeader, text="Select Course: ", font=5, fg="#fff", bg="#9badcc")
        lblSelectStudentCourse.place(x=xViewStudent, y=yViewStudent+50)
        
        viewStudentCourseDrop = OptionMenu(ViewStudentHeader,var5,*viewStudentCourseList)
        viewStudentCourseDrop.config(width=20)
        viewStudentCourseDrop.place(x=xViewStudent+150, y=yViewStudent+50)
    
    var4.trace('w', changedVar4)
    
    viewStudentDeptDrop = OptionMenu(ViewStudentHeader,var4,*viewStudentDeptList)
    viewStudentDeptDrop.config(width=30)
    viewStudentDeptDrop.place(x=xViewStudent+150, y=yViewStudent)
    
    

    #####View course frame ends
# 








def callRegisterStudentsScreen():
    global registerStudentScreen 
    global exitImage, refreshImage, addImage, recordImage, enrollImage, registerStudentsImage, viewStudentImage
    global editStudentImage, historyImage, viewCourseDetailsImage, resetImage
    global RegisterCameraImage, RegisterCaptureImage, RegisterImage
    
    registerStudentScreen = Toplevel(loginScreen)
    registerStudentScreen.geometry("1200x600")
    registerStudentScreen.title("")
    screens.append(registerStudentScreen)
    withdrawAll(registerStudentScreen)
    alignScreen(registerStudentScreen)
    registerStudentScreen.deiconify()
    c = Canvas(registerStudentScreen, bg="#9badcc", width="1200", height="600")
    c.place(x=0, y=0)
    lblFrameHeader = LabelFrame(registerStudentScreen, bg="#4285f4", text=" Home Screen ", font="10", fg="#fff")
    lblFrameHeader.pack(fill="both", expand="no")
    lblHeader = Label(lblFrameHeader, text = "FACIAL RECOGNITION ATTENDANCE SYSTEM", width=100 \
                      , height="1", font=2, bg="#4285f4", fg="#fff")
    lblHeader.pack()
     
    exitImage = PhotoImage(file="icons/page_back.png")
    btnExit = tk.Button(lblFrameHeader, text="EXIT", width=50, fg="#fff", bg="#4285f4", \
                 relief=FLAT, image=exitImage, compound="left", command=lambda: closeApp())
    btnExit.place(x=0, y=0)
     
    refreshImage = PhotoImage(file="icons/page_refresh.png")
    btnRefresh = tk.Button(lblFrameHeader, text="Refresh", width=50, fg="#fff", bg="#4285f4", \
                 relief=FLAT, image=refreshImage, compound="left")
    btnRefresh.place(x=90, y=0)
     
    actionsFrame = Frame(registerStudentScreen, bg="#fff", height="550", width="300")
    actionsFrame.place(x=20, y=60)
     
    actionsHeader = LabelFrame(actionsFrame, bg="#d8dde6", text=" ACTIONS ", height="500", width="300"\
                            ,fg="red", font="10")
    actionsHeader.pack(fill="both", expand="no")
     
    xAction = 5
    yAction = 10
     
    addImage = PhotoImage(file="icons/page_add.png")
    btnAddCourse = tk.Button(actionsHeader, text=" Add a Course", width="100", fg="red", relief=FLAT, image=addImage, \
                             compound="left", command=lambda: callAddCourseScreen())
    btnAddCourse.place(x=xAction, y=yAction)
    recordImage = PhotoImage(file="icons/page_save.png")
    btnRecord = tk.Button(actionsHeader, text=" Record Attendance", width="130", fg="red", relief=FLAT, image=recordImage, \
                          compound="left", command=lambda: callRecordCourseAttendanceScreen())
    btnRecord.place(x=xAction, y=yAction+30)
    enrollImage = PhotoImage(file="icons/page_white_put.png")
    btnEnroll= tk.Button(actionsHeader, text=" Enroll/Remove Students for a Course", width="230", fg="red", relief=FLAT, image=enrollImage, \
                             compound="left", command=lambda:callEnrollStudentScreen())
    btnEnroll.place(x=xAction, y=yAction+60)
    registerStudentsImage = PhotoImage(file="icons/page_attach.png")
    btnRegisterStudents= tk.Button(actionsHeader, text=" Register Students ", width="120", fg="red", relief=FLAT, image=registerStudentsImage, \
                             compound="left", command=lambda:callRegisterStudentsScreen())
    btnRegisterStudents.place(x=xAction, y=yAction+90)
    viewStudentImage = PhotoImage(file="icons/page_white_magnify.png")
    btnViewStudent = tk.Button(actionsHeader, text=" View Student ", width="100", fg="red", relief=FLAT, image=viewStudentImage, \
                             compound="left", command=lambda:callViewStudentScreen())
    btnViewStudent.place(x=xAction, y=yAction+120)
    editStudentImage = PhotoImage(file="icons/page_white_edit.png")
    btnEditStudent = tk.Button(actionsHeader, text=" Edit/Remove Student ", width="140", fg="red", relief=FLAT, image=editStudentImage, \
                             compound="left", command=lambda: callEditStudentScreen())
    btnEditStudent.place(x=xAction, y=yAction+150)
    viewCourseDetailsImage = PhotoImage(file="icons/page_white_find.png")
    btnViewCourseDetails = tk.Button(actionsHeader, text=" View Course Details ", width="135", fg="red", relief=FLAT, image=viewCourseDetailsImage, \
                             compound="left", command=lambda:callViewCourseScreen())
    btnViewCourseDetails.place(x=xAction, y=yAction+180)
    historyImage = PhotoImage(file="icons/folder.png")
    btnHistory = tk.Button(actionsHeader, text=" History", width="65", fg="red", relief=FLAT, image=historyImage, \
                             compound="left", command=lambda: callHistoryScreen())
    btnHistory.place(x=xAction, y=yAction+210) 
    resetImage = PhotoImage(file="icons/page_white_delete.png")
    btnReset = tk.Button(actionsHeader, text=" Reset App", width="80", fg="red", relief=FLAT, image=resetImage, \
                             compound="left")
    btnReset.place(x=xAction, y=yAction+240) 
     
     
     
    #####Register Students
    RegFrame = Frame(registerStudentScreen, bg="#9badcc", height="500", width="800")
    RegFrame.place(x=350, y=50)
          
    RegHeader = LabelFrame(RegFrame, text=" Register Student ", font="8", bg="#9badcc", \
                           height="500", width="800", fg="red")
    RegHeader.pack(fill="both", expand="no")
          
    xReg= 325
    yReg = 60
    #if ResizedImgReg exists,display image, else display default
    if(os.path.exists("ResizedImgReg.png") == False):
        imgfilename = PhotoImage(file = "BlankImage.png")
    else: 
        imgfilename = PhotoImage(file = "ResizedImgReg.png")  
    loginScreen.imgfilename = imgfilename
    cvFrame = Frame(RegHeader, bg="#9badcc", \
                           height="200", width="200")
    cvFrame.place(x=300, y=10)  
    cvImage = Canvas(cvFrame, height=200, width=200) 
#     cvImage.place(x=xReg, y=yReg)
    cvImage.pack(fill="both", expand=1)
    cvImage.create_image(0, 0, anchor=NW, image=imgfilename)
      
    RegisterCameraImage = PhotoImage(file="icons/page_white_camera.png")
    btnCamera = tk.Button(RegHeader, text="Camera", width="80", image = RegisterCameraImage, \
                          compound="left", command=lambda: captureRegImage())
    btnCamera.place(x=xReg+30, y=yReg+160)
      
#     RegisterCaptureImage = PhotoImage(file="icons/film.png") 
#     btnCapture = Button(RegHeader, text="Capture", width="60", fg="red", image = RegisterCaptureImage, \
#                         compound="left")
#     btnCapture.place(x=xReg+90, y=yReg+160)
    lblRegMessage = Label(RegFrame, text="Please capture image before filling this form: ", font=3, fg="red", bg="#9badcc")
    lblRegMessage.place(x=xReg-200, y=yReg+210)
    
    lblRegFirstName = Label(RegFrame, text="First Name: ", font=5, fg="#fff", bg="#9badcc")
    lblRegFirstName.place(x=xReg-200, y=yReg+235)
    txtRegFirstName= Entry(RegFrame, border=3, width=40)
    txtRegFirstName.place(x=xReg-100,y=yReg+235)
       
    lblRegLastName = Label(RegFrame, text="Last Name: ", font=5, fg="#fff", bg="#9badcc")
    lblRegLastName.place(x=xReg-200, y=yReg+270)
    txtRegLastName= Entry(RegFrame, border=3, width=40)
    txtRegLastName.place(x=xReg-100,y=yReg+270)

    lblRegSelectDept = Label(RegFrame, text="Select Department: ", font=5, fg="#fff", bg="#9badcc")
    lblRegSelectDept.place(x=xReg-200, y=yReg+300)
    
    department = getDepts()
    var2 = StringVar()
    deptdrop = OptionMenu(RegFrame,var2,*department)
    deptdrop.place(x=xReg-50, y=yReg+300)
    
    lblRegIDNumber = Label(RegFrame, text="ID Number: ", font=5, fg="#fff", bg="#9badcc")
    lblRegIDNumber.place(x=xReg-200, y=yReg+335)
    txtRegIDNumber= Entry(RegFrame, border=3, width=40)
    txtRegIDNumber.place(x=xReg-100,y=yReg+335)
    
    RegisterImage = PhotoImage(file="icons/page_save.png")
    btnSaveCapture = Button(RegHeader, text="Register", width="90", font="1", image=RegisterImage, \
                            compound="left", command=lambda: uploadStudent(txtRegFirstName.get(), txtRegLastName.get(), var2.get(), txtRegIDNumber.get()))
    btnSaveCapture.place(x=xReg+30, y=yReg+360)
    #####Register Students

def callRecordAttendanceScreen():
    global recordAttendanceScreen
    recordAttendanceScreen = Toplevel(loginScreen)
    recordAttendanceScreen.geometry("1200x600")
    recordAttendanceScreen.title("")
    screens.append(recordAttendanceScreen)
    withdrawAll(recordAttendanceScreen)
    alignScreen(recordAttendanceScreen)
    recordAttendanceScreen.deiconify()
    c = Canvas(recordAttendanceScreen, bg="#9badcc", width="1200", height="600")
    c.place(x=0, y=0)
    lblFrameHeader = LabelFrame(recordAttendanceScreen, bg="#4285f4", text=" Record Attendance ", font="10", fg="#fff")
    lblFrameHeader.pack(fill="both", expand="no")
    lblHeader = Label(lblFrameHeader, text = "FACIAL RECOGNITION ATTENDANCE SYSTEM", width=100 \
                      , height="1", font=2, bg="#4285f4", fg="#fff")
    lblHeader.pack()
     
    btnExit = Button(lblFrameHeader, text="Close", width=6, fg="#fff", bg="#4285f4", \
                 relief=FLAT, command=lambda: restart_app())
    btnExit.place(x=0, y=0)
     
    btnRefresh = Button(lblFrameHeader, text="Refresh", width=8, fg="#fff", bg="#4285f4", \
                 relief=FLAT)
    btnRefresh.place(x=90, y=0)
     
     
    #####Course Details Frame Starts
    courseDetailsFrame = Frame(recordAttendanceScreen, bg="#fff", height="550", width="400")
    courseDetailsFrame.place(x=20, y=60)
     
    courseDetailsHeader = LabelFrame(courseDetailsFrame, bg="#d8dde6", text=" Course Details ", height="500", width="400"\
                            ,fg="red", font="10")
    courseDetailsHeader.pack(fill="both", expand="no")
     
    xCourse = 10
    yCourse = 10
    courseCode = "EEE502"
    courseTitle = "Power Electronics "
    dept = "Electrical/Electronics Engineering"
    faculty = "Engineering"
    courseLecturer = "Aniebiet Akpan"
    enrollTimeStart = "12:00"
    enrollTimeEnd = "13:00"
     
    lblCourseCode = Label(courseDetailsHeader, text="Course Code: ", bg="#d8dde6")
    lblCourseCode.place(x=xCourse, y=yCourse)
    lblCourseCodeValue = Label(courseDetailsHeader, text=courseCode)
    lblCourseCodeValue.place(x=xCourse+80, y=yCourse)
     
    lblCourseTitle = Label(courseDetailsHeader, text="Course Title: ", bg="#d8dde6")
    lblCourseTitle.place(x=xCourse, y=yCourse+30)
    lblCourseTitleValue = Label(courseDetailsHeader, text=courseTitle, width="40", justify=LEFT, anchor=W)
    lblCourseTitleValue.place(x=xCourse+80, y=yCourse+30)
     
    lblDept = Label(courseDetailsHeader, text="Department: ", bg="#d8dde6")
    lblDept.place(x=xCourse, y=yCourse+60)
    lblDeptValue = Label(courseDetailsHeader, text=dept, width="40", justify=LEFT, anchor=W)
    lblDeptValue.place(x=xCourse+80, y=yCourse+60)
     
    lblFaculty = Label(courseDetailsHeader, text="Faculty: ", bg="#d8dde6")
    lblFaculty.place(x=xCourse, y=yCourse+90)
    lblFacultyValue = Label(courseDetailsHeader, text=faculty, width="40", justify=LEFT, anchor=W)
    lblFacultyValue.place(x=xCourse+80, y=yCourse+90)
     
    lblCourseLecturer = Label(courseDetailsHeader, text="Course Lecturer: ", bg="#d8dde6")
    lblCourseLecturer.place(x=xCourse, y=yCourse+120)
    lblCourseLecturerValue = Label(courseDetailsHeader, text=courseLecturer, width="30", justify=LEFT, anchor=W)
    lblCourseLecturerValue.place(x=xCourse+100, y=yCourse+120)
     
    lblDuration = Label(courseDetailsHeader, text="Duration: ", bg="#d8dde6", \
                        underline=10, font="10", fg="red")
    lblDuration.place(x=xCourse, y=yCourse+180)
     
    lblStartTime = Label(courseDetailsHeader, text="Enroll Start Time: ", bg="#d8dde6")
    lblStartTime.place(x=xCourse, y=yCourse+210)
    lblStartTimeValue = Label(courseDetailsHeader, text=enrollTimeStart, width="30", justify=LEFT, anchor=W)
    lblStartTimeValue.place(x=xCourse+100, y=yCourse+210)
    # 
    lblEndTime = Label(courseDetailsHeader, text="Enroll End Time: ", bg="#d8dde6")
    lblEndTime.place(x=xCourse, y=yCourse+240)
    lblEndTimeValue = Label(courseDetailsHeader, text=enrollTimeEnd, width="30", justify=LEFT, anchor=W)
    lblEndTimeValue.place(x=xCourse+100, y=yCourse+240)
    #####Course Details Frame Ends
     
     
    ###### Enroll frame start
    xEnroll = 275
    yEnroll = 10
    enrollFrame = Frame(recordAttendanceScreen, bg="#9badcc", height="500", width="700")
    enrollFrame.place(x=450, y=50)
        
    enrollHeader = LabelFrame(enrollFrame, text=" Record Attendance ", font="8", \
                               bg="#9badcc", fg="#fff", height="500", width="700")
    enrollHeader.pack(fill="both", expand="no")
    cvImage = Canvas(enrollHeader, bg="#fff", height=150, width=150)
    cvImage.place(x=xEnroll, y=yEnroll)
     
    lblEnroll = Label(enrollHeader, text="Click the button below to Enroll", fg="red", bg="#9badcc")
    lblEnroll.place(x=xEnroll-10, y=yEnroll+160)
     
    btnEnroll = Button(enrollHeader, text="Enroll", width="10", font="2", relief=FLAT)
    btnEnroll.place(x=xEnroll+25, y=yEnroll+190)
     
    ##Enrolled Frame start
    eFirstName = "Elniebiet"
    eLastName = "Akpan"
    eDept = "Electrical/Electronics Engineering"
    eFaculty = "Engineering"
     
    xEnrolled = 50
    yEnrolled = 280
    enrolledFrame = Frame(enrollFrame, bg="#d8dde6", height="200", width="600")
    enrolledFrame.place(x=xEnrolled, y=yEnrolled)
     
    labelSuccess = Label(enrollFrame, text="You have been enrolled successfully!", fg="green", bg="#d8dde6")
    labelSuccess.place(x=xEnrolled+10, y=yEnrolled)
     
    lblFirstName = Label(enrollFrame, text="First name: ", bg="#d8dde6")
    lblFirstName.place(x=xEnrolled+10, y=yEnrolled+30)
    lblFirstNameValue = Label(enrollFrame, text=eFirstName, width="70", anchor=W)
    lblFirstNameValue.place(x=xEnrolled+80, y=yEnrolled+30)
     
    lblLastName = Label(enrollFrame, text="Last name: ", bg="#d8dde6")
    lblLastName.place(x=xEnrolled+10, y=yEnrolled+60)
    lblLastNameValue = Label(enrollFrame, text=eLastName, width="70", anchor=W)
    lblLastNameValue.place(x=xEnrolled+80, y=yEnrolled+60)
     
    lblEDept = Label(enrollFrame, text="Department: ", bg="#d8dde6")
    lblEDept.place(x=xEnrolled+10, y=yEnrolled+90)
    lblEDeptValue = Label(enrollFrame, text=eDept, width="70", anchor=W)
    lblEDeptValue.place(x=xEnrolled+80, y=yEnrolled+90)
     
    lblEFaculty = Label(enrollFrame, text="Faculty: ", bg="#d8dde6")
    lblEFaculty.place(x=xEnrolled+10, y=yEnrolled+120)
    lblEFacultyValue = Label(enrollFrame, text=eFaculty, width="70", anchor=W)
    lblEFacultyValue.place(x=xEnrolled+80, y=yEnrolled+120)
# 

def callHistoryScreen():
    global historyScreen 
    global exitImage, refreshImage, addImage, recordImage, enrollImage, registerStudentsImage, viewStudentImage
    global editStudentImage, historyImage, viewCourseDetailsImage, resetImage

    historyScreen = Toplevel(loginScreen)
    historyScreen.geometry("1200x600")
    historyScreen.title("")
    screens.append(historyScreen)
    withdrawAll(historyScreen)
    alignScreen(historyScreen)
    historyScreen.deiconify()
    c = Canvas(historyScreen, bg="#9badcc", width="1200", height="600")
    c.place(x=0, y=0)
    lblFrameHeader = LabelFrame(historyScreen, bg="#4285f4", text=" Home Screen ", font="10", fg="#fff")
    lblFrameHeader.pack(fill="both", expand="no")
    lblHeader = Label(lblFrameHeader, text = "FACIAL RECOGNITION ATTENDANCE SYSTEM", width=100 \
                      , height="1", font=2, bg="#4285f4", fg="#fff")
    lblHeader.pack()
     
    exitImage = PhotoImage(file="icons/page_back.png")
    btnExit = tk.Button(lblFrameHeader, text="EXIT", width=50, fg="#fff", bg="#4285f4", \
                 relief=FLAT, image=exitImage, compound="left", command=lambda: closeApp())
    btnExit.place(x=0, y=0)
     
    refreshImage = PhotoImage(file="icons/page_refresh.png")
    btnRefresh = tk.Button(lblFrameHeader, text="Refresh", width=50, fg="#fff", bg="#4285f4", \
                 relief=FLAT, image=refreshImage, compound="left")
    btnRefresh.place(x=90, y=0)
     
    actionsFrame = Frame(historyScreen, bg="#fff", height="550", width="300")
    actionsFrame.place(x=20, y=60)
     
    actionsHeader = LabelFrame(actionsFrame, bg="#d8dde6", text=" ACTIONS ", height="500", width="300"\
                            ,fg="red", font="10")
    actionsHeader.pack(fill="both", expand="no")
     
    xAction = 5
    yAction = 10
     
    addImage = PhotoImage(file="icons/page_add.png")
    btnAddCourse = tk.Button(actionsHeader, text=" Add a Course", width="100", fg="red", relief=FLAT, image=addImage, \
                             compound="left", command=lambda: callAddCourseScreen())
    btnAddCourse.place(x=xAction, y=yAction)
    recordImage = PhotoImage(file="icons/page_save.png")
    btnRecord = tk.Button(actionsHeader, text=" Record Attendance", width="130", fg="red", relief=FLAT, image=recordImage, \
                          compound="left", command=lambda: callRecordCourseAttendanceScreen())
    btnRecord.place(x=xAction, y=yAction+30)
    enrollImage = PhotoImage(file="icons/page_white_put.png")
    btnEnroll= tk.Button(actionsHeader, text=" Enroll/Remove Students for a Course", width="230", fg="red", relief=FLAT, image=enrollImage, \
                             compound="left", command=lambda:callEnrollStudentScreen())
    btnEnroll.place(x=xAction, y=yAction+60)
    registerStudentsImage = PhotoImage(file="icons/page_attach.png")
    btnRegisterStudents= tk.Button(actionsHeader, text=" Register Students ", width="120", fg="red", relief=FLAT, image=registerStudentsImage, \
                             compound="left", command=lambda:callRegisterStudentsScreen())
    btnRegisterStudents.place(x=xAction, y=yAction+90)
    viewStudentImage = PhotoImage(file="icons/page_white_magnify.png")
    btnViewStudent = tk.Button(actionsHeader, text=" View Student ", width="100", fg="red", relief=FLAT, image=viewStudentImage, \
                             compound="left", command=lambda:callViewStudentScreen())
    btnViewStudent.place(x=xAction, y=yAction+120)
    editStudentImage = PhotoImage(file="icons/page_white_edit.png")
    btnEditStudent = tk.Button(actionsHeader, text=" Edit/Remove Student ", width="140", fg="red", relief=FLAT, image=editStudentImage, \
                             compound="left", command=lambda: callEditStudentScreen())
    btnEditStudent.place(x=xAction, y=yAction+150)
    viewCourseDetailsImage = PhotoImage(file="icons/page_white_find.png")
    btnViewCourseDetails = tk.Button(actionsHeader, text=" View Course Details ", width="135", fg="red", relief=FLAT, image=viewCourseDetailsImage, \
                             compound="left", command=lambda:callViewCourseScreen())
    btnViewCourseDetails.place(x=xAction, y=yAction+180)
    historyImage = PhotoImage(file="icons/folder.png")
    btnHistory = tk.Button(actionsHeader, text=" History", width="65", fg="red", relief=FLAT, image=historyImage, \
                             compound="left", command=lambda: callHistoryScreen())
    btnHistory.place(x=xAction, y=yAction+210) 
    resetImage = PhotoImage(file="icons/page_white_delete.png")
    btnReset = tk.Button(actionsHeader, text=" Reset App", width="80", fg="red", relief=FLAT, image=resetImage, \
                             compound="left")
    btnReset.place(x=xAction, y=yAction+240) 
     
     
    ###### history frame start
    historyFrame = Frame(historyScreen, bg="#9badcc", height="400", width="500")
    historyFrame.place(x=400, y=100)
           
    historyHeader = LabelFrame(historyFrame, text=" History Log ", font="8", bg="#9badcc", fg="#fff", height="600", width="500")
    historyHeader.pack(fill="both", expand="no")
          
    sclHistory = Scrollbar(historyHeader)
    sclHistory.pack(side=RIGHT, fill=Y)
          
    historyList = Listbox(historyHeader, yscrollcommand = sclHistory.set, width="80", height="25")
    historyList.insert(END, "There is currently no history")
    historyList.insert(END, "")
    historyList.pack( side = LEFT, fill = BOTH )
    sclHistory.config( command = historyList.yview )
    ##### hostory frame end

def callEditStudentScreen():
    global registerStudentScreen 
    global exitImage, refreshImage, addImage, recordImage, enrollImage, registerStudentsImage, viewStudentImage
    global editStudentImage, historyImage, viewCourseDetailsImage, resetImage
    global RegisterCameraImage, RegisterCaptureImage, RegisterImage
    
    registerStudentScreen = Toplevel(loginScreen)
    registerStudentScreen.geometry("1200x600")
    registerStudentScreen.title("")
    screens.append(registerStudentScreen)
    withdrawAll(registerStudentScreen)
    alignScreen(registerStudentScreen)
    registerStudentScreen.deiconify()
    c = Canvas(registerStudentScreen, bg="#9badcc", width="1200", height="600")
    c.place(x=0, y=0)
    lblFrameHeader = LabelFrame(registerStudentScreen, bg="#4285f4", text=" Home Screen ", font="10", fg="#fff")
    lblFrameHeader.pack(fill="both", expand="no")
    lblHeader = Label(lblFrameHeader, text = "FACIAL RECOGNITION ATTENDANCE SYSTEM", width=100 \
                      , height="1", font=2, bg="#4285f4", fg="#fff")
    lblHeader.pack()
     
    exitImage = PhotoImage(file="icons/page_back.png")
    btnExit = tk.Button(lblFrameHeader, text="EXIT", width=50, fg="#fff", bg="#4285f4", \
                 relief=FLAT, image=exitImage, compound="left", command=lambda: closeApp())
    btnExit.place(x=0, y=0)
     
    refreshImage = PhotoImage(file="icons/page_refresh.png")
    btnRefresh = tk.Button(lblFrameHeader, text="Refresh", width=50, fg="#fff", bg="#4285f4", \
                 relief=FLAT, image=refreshImage, compound="left")
    btnRefresh.place(x=90, y=0)
     
    actionsFrame = Frame(registerStudentScreen, bg="#fff", height="550", width="300")
    actionsFrame.place(x=20, y=60)
     
    actionsHeader = LabelFrame(actionsFrame, bg="#d8dde6", text=" ACTIONS ", height="500", width="300"\
                            ,fg="red", font="10")
    actionsHeader.pack(fill="both", expand="no")
     
    xAction = 5
    yAction = 10
     
    addImage = PhotoImage(file="icons/page_add.png")
    btnAddCourse = tk.Button(actionsHeader, text=" Add a Course", width="100", fg="red", relief=FLAT, image=addImage, \
                             compound="left", command=lambda: callAddCourseScreen())
    btnAddCourse.place(x=xAction, y=yAction)
    recordImage = PhotoImage(file="icons/page_save.png")
    btnRecord = tk.Button(actionsHeader, text=" Record Attendance", width="130", fg="red", relief=FLAT, image=recordImage, \
                          compound="left", command=lambda: callRecordCourseAttendanceScreen())
    btnRecord.place(x=xAction, y=yAction+30)
    enrollImage = PhotoImage(file="icons/page_white_put.png")
    btnEnroll= tk.Button(actionsHeader, text=" Enroll/Remove Students for a Course", width="230", fg="red", relief=FLAT, image=enrollImage, \
                             compound="left", command=lambda:callEnrollStudentScreen())
    btnEnroll.place(x=xAction, y=yAction+60)
    registerStudentsImage = PhotoImage(file="icons/page_attach.png")
    btnRegisterStudents= tk.Button(actionsHeader, text=" Register Students ", width="120", fg="red", relief=FLAT, image=registerStudentsImage, \
                             compound="left", command=lambda:callRegisterStudentsScreen())
    btnRegisterStudents.place(x=xAction, y=yAction+90)
    viewStudentImage = PhotoImage(file="icons/page_white_magnify.png")
    btnViewStudent = tk.Button(actionsHeader, text=" View Student ", width="100", fg="red", relief=FLAT, image=viewStudentImage, \
                             compound="left", command=lambda:callViewStudentScreen())
    btnViewStudent.place(x=xAction, y=yAction+120)
    editStudentImage = PhotoImage(file="icons/page_white_edit.png")
    btnEditStudent = tk.Button(actionsHeader, text=" Edit/Remove Student ", width="140", fg="red", relief=FLAT, image=editStudentImage, \
                             compound="left", command=lambda: callEditStudentScreen())
    btnEditStudent.place(x=xAction, y=yAction+150)
    viewCourseDetailsImage = PhotoImage(file="icons/page_white_find.png")
    btnViewCourseDetails = tk.Button(actionsHeader, text=" View Course Details ", width="135", fg="red", relief=FLAT, image=viewCourseDetailsImage, \
                             compound="left", command=lambda:callViewCourseScreen())
    btnViewCourseDetails.place(x=xAction, y=yAction+180)
    historyImage = PhotoImage(file="icons/folder.png")
    btnHistory = tk.Button(actionsHeader, text=" History", width="65", fg="red", relief=FLAT, image=historyImage, \
                             compound="left", command=lambda: callHistoryScreen())
    btnHistory.place(x=xAction, y=yAction+210) 
    resetImage = PhotoImage(file="icons/page_white_delete.png")
    btnReset = tk.Button(actionsHeader, text=" Reset App", width="80", fg="red", relief=FLAT, image=resetImage, \
                             compound="left")
    btnReset.place(x=xAction, y=yAction+240) 
     
     
     
    #####Edit Students
    RegFrame = Frame(registerStudentScreen, bg="#9badcc", height="500", width="800")
    RegFrame.place(x=350, y=50)
          
    RegHeader = LabelFrame(RegFrame, text=" Edit Student Details ", font="8", bg="#9badcc", \
                           height="500", width="800", fg="red")
    RegHeader.pack(fill="both", expand="no")
    
    #select student start
    xViewStudent= 20
    yViewStudent = 30
    
    xReg= 325
    yReg = 60
    numAttendance = 0
        
    lblSelectStudentDept = Label(RegHeader, text="Select Department: ", font=5, fg="#fff", bg="#9badcc")
    lblSelectStudentDept.place(x=xViewStudent, y=yViewStudent)
    
    
    viewStudentDeptList = getDepts()
    var4 = StringVar()
    def changedVar4(*args):
        studentsList = []
        viewStudentsList = []
        selectedDeptVar4 = var4.get()
        studentsList = getStudentsList(selectedDeptVar4)
        count = 0
        idList = []
        for each in studentsList:
            idList.append(studentsList[count][0])
            count = count+1
        print(idList)
        print("Studentslist is ")
        print(idList)
        if len(idList) == 0:
            viewStudentsList = ['select']
        else:
            viewStudentsList = idList
        var6 = StringVar()
        def changedVar6(*args):
            selectedStudentVar6 = var6.get()
#                 get student details
            getDet = EditStudent.EditStudent()
            con = pymysql.connect(host="localhost", user="phpmyadmin", passwd="galileo123", db="attendance_db")
            stDet = getDet.getStudentDetails(con, selectedDeptVar4, selectedStudentVar6)
            print("StDet is ")
            print(stDet)
            stID = StringVar()
            stFirstName = StringVar()
            stLastName = StringVar()
            stImageName = StringVar()
            
            if stDet == None:
                stID = ''
                stFirstName = ''
                stLastName = ''
                stImageName = ''
            else:
                stID = stDet[0][0]
                stFirstName = stDet[0][1]
                stLastName = stDet[0][2]
                stImageName = "students/Resized"+stDet[0][3]
            #select student end
            #display image
            if(os.path.exists(stImageName) == False):
                imgfilename = PhotoImage(file = "BlankImage.png")
            else: 
                imgfilename = PhotoImage(file = stImageName)  
            loginScreen.imgfilename = imgfilename
            cvFrame = Frame(RegHeader, bg="#9badcc", \
                                       height="200", width="200")
            cvFrame.place(x=400, y=10)  
            cvImage = Canvas(cvFrame, height=200, width=200) 
            #     cvImage.place(x=xReg, y=yReg)
            cvImage.pack(fill="both", expand=1)
            cvImage.create_image(0, 0, anchor=NW, image=imgfilename)
            
            #load form

            lblRegMessage = Label(RegFrame, text="Please fill in valid details: ", font=3, fg="red", bg="#9badcc")
            lblRegMessage.place(x=xReg-200, y=yReg+210)
            
            lblRegFirstName = Label(RegFrame, text="First Name: ", font=5, fg="#fff", bg="#9badcc")
            lblRegFirstName.place(x=xReg-200, y=yReg+235)
            txtRegFirstName= Text(RegFrame, height=1, border=3, width=50)
            txtRegFirstName.place(x=xReg-100,y=yReg+235)
            setText(txtRegFirstName, stFirstName)
            lblRegLastName = Label(RegFrame, text="Last Name: ", font=5, fg="#fff", bg="#9badcc")
            lblRegLastName.place(x=xReg-200, y=yReg+270)
            txtRegLastName= Text(RegFrame, height=1, border=3, width=50)
            txtRegLastName.place(x=xReg-100,y=yReg+270)
            setText(txtRegLastName, stLastName)
            
            lblRegIDNumber = Label(RegFrame, text="ID Number: ", font=5, fg="#fff", bg="#9badcc")
            lblRegIDNumber.place(x=xReg-200, y=yReg+300)
            txtRegIDNumber= Text(RegFrame, height=1, border=3, width=50)
            txtRegIDNumber.place(x=xReg-100,y=yReg+300)
            setText(txtRegIDNumber, stID)
            txtRegIDNumber.config(state="disabled")
#             RegisterImage = PhotoImage(file="icons/page_save.png")
            btnUpdateStudent = Button(RegHeader, text="Update", width="15", font="1", \
                                    compound="left", command=lambda: updateStudent(txtRegFirstName.get(1.0, "end-1c"), txtRegLastName.get(1.0, "end-1c"), txtRegIDNumber.get(1.0, "end-1c"), var4.get(), var6.get()))
            
            btnUpdateStudent.place(x=xReg-100, y=yReg+320)  
            
            btnRemoveStudent = Button(RegHeader, text="Remove Student", width="15", font="1", \
                                    compound="left", command=lambda: removeStudent(txtRegIDNumber.get(1.0, "end-1c"), stFirstName))
            
            btnRemoveStudent.place(x=xReg+80, y=yReg+320)
            #end form
    


        var6.trace('w', changedVar6)
        
        lblSelectStudentCourse = Label(RegHeader, text="Select Student: ", font=5, fg="#fff", bg="#9badcc")
        lblSelectStudentCourse.place(x=xViewStudent, y=yViewStudent+50)
    
        viewStudentNameDrop = OptionMenu(RegHeader,var6,*viewStudentsList)
        viewStudentNameDrop.config(width=20)
        viewStudentNameDrop.place(x=xViewStudent+150, y=yViewStudent+50)
            
    var4.trace('w', changedVar4)
    
    viewStudentDeptDrop = OptionMenu(RegHeader,var4,*viewStudentDeptList)
    viewStudentDeptDrop.config(width=20)
    viewStudentDeptDrop.place(x=xViewStudent+150, y=yViewStudent)
      
    
    
    #####Edit Students
    #
    #
def callAddCourseScreen():
    global addCourseScreen
    global exitImage, refreshImage, addImage, recordImage, enrollImage, registerStudentsImage, viewStudentImage
    global editStudentImage, historyImage, viewCourseDetailsImage, resetImage, addCourseImage

    addCourseScreen = Toplevel(loginScreen)
    addCourseScreen.geometry("1200x600")
    addCourseScreen.title("")
    screens.append(addCourseScreen)
    withdrawAll(addCourseScreen)
    alignScreen(addCourseScreen)
    addCourseScreen.deiconify()
    c = Canvas(addCourseScreen, bg="#9badcc", width="1200", height="600")
    c.place(x=0, y=0)
    lblFrameHeader = LabelFrame(addCourseScreen, bg="#4285f4", text=" Home Screen ", font="10", fg="#fff")
    lblFrameHeader.pack(fill="both", expand="no")
    lblHeader = Label(lblFrameHeader, text = "FACIAL RECOGNITION ATTENDANCE SYSTEM", width=100 \
                      , height="1", font=2, bg="#4285f4", fg="#fff")
    lblHeader.pack()
     
    exitImage = PhotoImage(file="icons/page_back.png")
    btnExit = tk.Button(lblFrameHeader, text="EXIT", width=50, fg="#fff", bg="#4285f4", \
                 relief=FLAT, image=exitImage, compound="left", command=lambda: closeApp())
    btnExit.place(x=0, y=0)
     
    refreshImage = PhotoImage(file="icons/page_refresh.png")
    btnRefresh = tk.Button(lblFrameHeader, text="Refresh", width=50, fg="#fff", bg="#4285f4", \
                 relief=FLAT, image=refreshImage, compound="left")
    btnRefresh.place(x=90, y=0)
     
    actionsFrame = Frame(addCourseScreen, bg="#fff", height="550", width="300")
    actionsFrame.place(x=20, y=60)
     
    actionsHeader = LabelFrame(actionsFrame, bg="#d8dde6", text=" ACTIONS ", height="500", width="300"\
                            ,fg="red", font="10")
    actionsHeader.pack(fill="both", expand="no")

    xAction = 5
    yAction = 10
     
    addImage = PhotoImage(file="icons/page_add.png")
    btnAddCourse = tk.Button(actionsHeader, text=" Add a Course", width="100", fg="red", relief=FLAT, image=addImage, \
                             compound="left", command=lambda: callAddCourseScreen())
    btnAddCourse.place(x=xAction, y=yAction)
    recordImage = PhotoImage(file="icons/page_save.png")
    btnRecord = tk.Button(actionsHeader, text=" Record Attendance", width="130", fg="red", relief=FLAT, image=recordImage, \
                          compound="left", command=lambda: callRecordCourseAttendanceScreen())
    btnRecord.place(x=xAction, y=yAction+30)
    enrollImage = PhotoImage(file="icons/page_white_put.png")
    btnEnroll= tk.Button(actionsHeader, text=" Enroll/Remove Students for a Course", width="230", fg="red", relief=FLAT, image=enrollImage, \
                             compound="left", command=lambda:callEnrollStudentScreen())
    btnEnroll.place(x=xAction, y=yAction+60)
    registerStudentsImage = PhotoImage(file="icons/page_attach.png")
    btnRegisterStudents= tk.Button(actionsHeader, text=" Register Students ", width="120", fg="red", relief=FLAT, image=registerStudentsImage, \
                             compound="left", command=lambda:callRegisterStudentsScreen())
    btnRegisterStudents.place(x=xAction, y=yAction+90)
    viewStudentImage = PhotoImage(file="icons/page_white_magnify.png")
    btnViewStudent = tk.Button(actionsHeader, text=" View Student ", width="100", fg="red", relief=FLAT, image=viewStudentImage, \
                             compound="left", command=lambda:callViewStudentScreen())
    btnViewStudent.place(x=xAction, y=yAction+120)
    editStudentImage = PhotoImage(file="icons/page_white_edit.png")
    btnEditStudent = tk.Button(actionsHeader, text=" Edit/Remove Student ", width="140", fg="red", relief=FLAT, image=editStudentImage, \
                             compound="left", command=lambda: callEditStudentScreen())
    btnEditStudent.place(x=xAction, y=yAction+150)
    viewCourseDetailsImage = PhotoImage(file="icons/page_white_find.png")
    btnViewCourseDetails = tk.Button(actionsHeader, text=" View Course Details ", width="135", fg="red", relief=FLAT, image=viewCourseDetailsImage, \
                             compound="left", command=lambda:callViewCourseScreen())
    btnViewCourseDetails.place(x=xAction, y=yAction+180)
    historyImage = PhotoImage(file="icons/folder.png")
    btnHistory = tk.Button(actionsHeader, text=" History", width="65", fg="red", relief=FLAT, image=historyImage, \
                             compound="left")
    btnHistory.place(x=xAction, y=yAction+210) 
    resetImage = PhotoImage(file="icons/page_white_delete.png")
    btnReset = tk.Button(actionsHeader, text=" Reset App", width="80", fg="red", relief=FLAT, image=resetImage, \
                             compound="left", command=lambda: callHistoryScreen())
    btnReset.place(x=xAction, y=yAction+240) 
     
     
    ######Add course Frame start
    AddCourse = Frame(addCourseScreen, bg="#9badcc", height="400", width="700")
    AddCourse.place(x=400, y=100)
           
    AddCourseHeader = LabelFrame(AddCourse, text=" Add A Course ", font="8", bg="#9badcc", height="400", width="700")
    AddCourseHeader.pack(fill="both", expand="no")
           
    xAddCourse= 20
    yAddCourse = 30
    global txtAddCourseCode, txtAddCourseTitle, txtAddCourseLecturer
    lblCourseCode = Label(AddCourse, text="Course Code: ", font=5, fg="#fff", bg="#9badcc")
    lblCourseCode.place(x=xAddCourse, y=yAddCourse)
    txtAddCourseCode= Entry(AddCourse, border=3, width=40)
    txtAddCourseCode.place(x=xAddCourse+110,y=yAddCourse)
          
    lblCourseTitle = Label(AddCourse, text="Course Title: ", font=5, fg="#fff", bg="#9badcc")
    lblCourseTitle.place(x=xAddCourse, y=yAddCourse+30)
    txtAddCourseTitle= Entry(AddCourse, border=3, width=40)
    txtAddCourseTitle.place(x=xAddCourse+110,y=yAddCourse+30)
       
    lbladdSelectDept = Label(AddCourse, text="Select Department: ", font=5, fg="#fff", bg="#9badcc")
    lbladdSelectDept.place(x=xAddCourse, y=yAddCourse+60)
#     addDeptList = ['Electrical/Electronics','Mechanical Engineering','Civil Engineering']
    addDeptList = getDepts();
    var3 = StringVar()
    addDeptDrop = OptionMenu(AddCourse,var3,*addDeptList)
    addDeptDrop.place(x=xAddCourse+160, y=yAddCourse+60)
          
    lblLecturer = Label(AddCourse, text="Lecturer: ", font=5, fg="#fff", bg="#9badcc")
    lblLecturer.place(x=xAddCourse, y=yAddCourse+100)
    txtAddCourseLecturer = Entry(AddCourse, border=3, width=40)
    txtAddCourseLecturer.place(x=xAddCourse+110,y=yAddCourse+100)
      
    addCourseImage = PhotoImage(file="icons/page_add.png")    
    btnAddCourse = tk.Button(AddCourse, text ="Add Course", height=25, font=5, width=130, \
                             image=addCourseImage, compound="left", command=lambda: addACourse(txtAddCourseCode.get().replace(" ", "").lower(), \
                             txtAddCourseTitle.get().strip(), var3.get(), txtAddCourseLecturer.get().strip()))
    btnAddCourse.place(x=yAddCourse+100,y=yAddCourse+150)
    
def callHomeScreen():
    global homeScreen
    global exitImage, refreshImage, addImage, recordImage, enrollImage, registerStudentsImage, viewStudentImage
    global editStudentImage, historyImage, viewCourseDetailsImage, resetImage
    
#     homeScreen = Toplevel(loginScreen)
#     screens.append(homeScreen)
#     withdrawAll(homeScreen)
# #     loginScreen.withdraw()
#     homeScreen.geometry("1200x600")
#     alignScreen(homeScreen)


    homeScreen = Toplevel(loginScreen)
    homeScreen.geometry("1200x600")
    homeScreen.title("")
    screens.append(homeScreen)
    withdrawAll(loginScreen)
    loginScreen.withdraw()
    alignScreen(homeScreen)
    homeScreen.deiconify()
    
    c = Canvas(homeScreen, bg="#9badcc", width="1200", height="600")
    c.place(x=0, y=0)
    lblFrameHeader = LabelFrame(homeScreen, bg="#4285f4", text=" Home Screen ", font="10", fg="#fff")
    lblFrameHeader.pack(fill="both", expand="no")
    lblHeader = Label(lblFrameHeader, text = "FACIAL RECOGNITION ATTENDANCE SYSTEM", width=100 \
                      , height="1", font=2, bg="#4285f4", fg="#fff")
    lblHeader.pack()
    
    exitImage = tk.PhotoImage(file="icons/page_back.png")
    btnExit = tk.Button(lblFrameHeader, text="EXIT", width=50, fg="#fff", bg="#4285f4", \
                 relief=FLAT, image=exitImage, compound="left", command=lambda: closeApp())
    btnExit.place(x=0, y=0)
    
    refreshImage = PhotoImage(file="icons/page_refresh.png")
    btnRefresh = tk.Button(lblFrameHeader, text="Refresh", width=50, fg="#fff", bg="#4285f4", \
                 relief=FLAT, image=refreshImage, compound="left", command=lambda: refreshApp(homeScreen))
    btnRefresh.place(x=90, y=0)
    
    actionsFrame = Frame(homeScreen, bg="#fff", height="550", width="300")
    actionsFrame.place(x=20, y=60)
    
    actionsHeader = LabelFrame(actionsFrame, bg="#d8dde6", text=" ACTIONS ", height="500", width="300"\
                            ,fg="red", font="10")
    actionsHeader.pack(fill="both", expand="no")
    
    xAction = 5
    yAction = 10
    
    addImage = PhotoImage(file="icons/page_add.png")
    btnAddCourse = tk.Button(actionsHeader, text=" Add a Course", width="100", fg="red", relief=FLAT, image=addImage, \
                             compound="left", command=lambda: callAddCourseScreen())
    btnAddCourse.place(x=xAction, y=yAction)
    recordImage = PhotoImage(file="icons/page_save.png")
    btnRecord = tk.Button(actionsHeader, text=" Record Attendance", width="130", fg="red", relief=FLAT, image=recordImage, \
                          compound="left", command=lambda: callRecordCourseAttendanceScreen())
    btnRecord.place(x=xAction, y=yAction+30)
    enrollImage = PhotoImage(file="icons/page_white_put.png")
    btnEnroll= tk.Button(actionsHeader, text=" Enroll/Remove Students for a Course", width="240", fg="red", relief=FLAT, image=enrollImage, \
                             compound="left", command=lambda:callEnrollStudentScreen())
    btnEnroll.place(x=xAction, y=yAction+60)
    registerStudentsImage = PhotoImage(file="icons/page_attach.png")
    btnRegisterStudents= tk.Button(actionsHeader, text=" Register Students ", width="120", fg="red", relief=FLAT, image=registerStudentsImage, \
                             compound="left", command=lambda:callRegisterStudentsScreen())
    btnRegisterStudents.place(x=xAction, y=yAction+90)
    viewStudentImage = PhotoImage(file="icons/page_white_magnify.png")
    btnViewStudent = tk.Button(actionsHeader, text=" View Student ", width="100", fg="red", relief=FLAT, image=viewStudentImage, \
                             compound="left", command=lambda:callViewStudentScreen())
    btnViewStudent.place(x=xAction, y=yAction+120)
    editStudentImage = PhotoImage(file="icons/page_white_edit.png")
    btnEditStudent = tk.Button(actionsHeader, text=" Edit/Remove Student ", width="140", fg="red", relief=FLAT, image=editStudentImage, \
                             compound="left", command=lambda: callEditStudentScreen())
    btnEditStudent.place(x=xAction, y=yAction+150)
    viewCourseDetailsImage = PhotoImage(file="icons/page_white_find.png")
    btnViewCourseDetails = tk.Button(actionsHeader, text=" View Course Details ", width="135", fg="red", relief=FLAT, image=viewCourseDetailsImage, \
                             compound="left", command=lambda:callViewCourseScreen())
    btnViewCourseDetails.place(x=xAction, y=yAction+180)
    historyImage = PhotoImage(file="icons/folder.png")
    btnHistory = tk.Button(actionsHeader, text=" History", width="65", fg="red", relief=FLAT, image=historyImage, \
                             compound="left", command=lambda: callHistoryScreen())
    btnHistory.place(x=xAction, y=yAction+210) 
    resetImage = PhotoImage(file="icons/page_white_delete.png")
    btnReset = tk.Button(actionsHeader, text=" Reset App", width="80", fg="red", relief=FLAT, image=resetImage, \
                             compound="left")
    btnReset.place(x=xAction, y=yAction+240) 
    
def callLogin():
    global loginScreen
    loginScreen = Tk()
    screens.append(loginScreen)
    withdrawAll(loginScreen)
    loginScreen.geometry("1200x600")
    loginScreen.title("")
    alignScreen(loginScreen)
    c = Canvas(loginScreen, bg="#9badcc", width="1200", height="600")
    c.place(x=0, y=0)
    lblFrameHeader = LabelFrame(loginScreen, bg="#4285f4", text=" Log In ", font="10", fg="#fff")
    lblFrameHeader.pack(fill="both", expand="no")
    lblHeader = Label(lblFrameHeader, text = "FACIAL RECOGNITION ATTENDANCE SYSTEM", width=100 \
                      , height="1", font=2, bg="#4285f4", fg="#fff")
    lblHeader.pack()
    
    exitImage = PhotoImage(file="icons/page_back.png")
    btnExit = tk.Button(lblFrameHeader, text="EXIT", width=50, fg="#fff", bg="#4285f4", \
                 relief=FLAT, image=exitImage, compound="left", command=lambda: closeApp())
    btnExit.place(x=0, y=0)
    
    
    helpPane = Frame(loginScreen, bg="#fff", height="500", width="350")
    helpPane.place(x=20, y=60)
    
    helpHeader = LabelFrame(helpPane, bg="#d8dde6", text="Help", height="500", width="350"\
                            ,fg="red", font="10")
    helpHeader.pack(fill="both", expand="no");
     
    loginFrame = Frame(loginScreen, bg="#9badcc", height="400", width="700")
    loginFrame.place(x=400, y=100)
    
    loginHeader = LabelFrame(loginFrame, text=" Please Login ", font="8", bg="#9badcc", height="400", width="700")
    loginHeader.pack(fill="both", expand="no")
    
    xcord = 150
    ycord = 120
    
    usernameImage = PhotoImage(file="icons/page_white_compressed.png")
    lblUsername = tk.Label(loginFrame, text="Username: ", font=5, image=usernameImage, compound="left")
    lblUsername.place(x=xcord, y=ycord)
    
    errorColor = "red"
    errorMessage = Label(loginFrame, text="Enter valid username and password (no spaces)", fg=errorColor, bg="yellow", font="1")
    errorMessage.place(x=xcord+10, y=ycord-40)
    
    txtUsername = Entry(loginFrame, border=3, width=40)
    txtUsername.place(x=xcord+120, y=ycord)
    
    passwordImage = PhotoImage(file="icons/page_white_key.png")
    lblPassword = tk.Label(loginFrame, text="Password: ", font=5, image=passwordImage, compound="left")
    lblPassword.place(x=xcord,y=ycord+30)
    
#     txtPassword = Text(loginFrame, height=1, border=3, width=30)
    txtPassword = Entry(loginFrame, border=3, width=40)
    txtPassword.config(show="*")
    txtPassword.place(x=xcord+120,y=ycord+30)
    loginImage = PhotoImage(file="icons/page_white_go.png")
    
    
    btnLogin = tk.Button(loginFrame, text ="Log In", height=25, font=5, width=80, image=loginImage, \
                         compound="left", command=lambda: checkLogin(txtUsername.get().replace(' ', ''), txtPassword.get()))
    btnLogin.place(x=xcord+85,y=ycord+70)
    loginScreen.mainloop()
callLogin()

