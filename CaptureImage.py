from tkinter import *
from tkinter import messagebox
from PIL import Image
from tkinter import PhotoImage
import cv2

class CaptureImage():
    def resizeImage(imgtoresize, imgtoresizename):
        openImage = Image.open(imgtoresize)
        newimg = openImage.resize((200, 200), Image.ANTIALIAS)
        newimg.save(imgtoresizename, "png")
        
    def capture(self, image_type):
        imgName = ""
        if image_type == "REG":
            imgName = "ImgReg.png"
        elif image_type == "ENROLL":
            imgName = "ImgEnroll.png"
        else:
            print("please select image task")
            return    
        try: 
            cam = cv2.VideoCapture(0)
            # cv2.namedWindow("Image Capture")
            while True:
                ret, frame = cam.read()
                #add button to frame
            #     rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.imshow(">>>>>>>>>>>>>> PRESS SPACEBAR TO CAPTURE <<<<<<<<<<<<<<<<", frame)
                if not ret:
                    break
                k = cv2.waitKey(1)
            
                if k%256 == 32:
                    # SPACE pressed
            #         img_name = "opencv_frame_{}.png".format(img_counter)
                    img_name = imgName
                    cv2.imwrite(img_name, frame)
                    print("{} written!".format(img_name))
                    CaptureImage.resizeImage(img_name, "Resized"+img_name)
                    break
            
            cam.release()
            cv2.destroyAllWindows()
            return 0
        except:
            messagebox.showinfo("Error", "couldn't load camera, please check that a Camera is plugged.")
            cv2.destroyAllWindows()
            return 1
# response = CaptureImage.capture("REG")
# response = CaptureImage.resizeImage("ImgReg.png", "resizedImage.png")