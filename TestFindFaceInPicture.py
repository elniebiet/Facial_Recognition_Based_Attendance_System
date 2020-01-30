import face_recognition
import re

# image = face_recognition.load_image_file('./img/groups/team2.jpg')
# face_locations = face_recognition.face_locations(image)
#
# # Array of coords of each face
# # print(face_locations)
#
# print(f'There are {len(face_locations)} people in this image')

image = face_recognition.load_image_file('./imgRecord.png')
face_locations = face_recognition.face_locations(image)

# Array of coords of each face
# print(face_locations)

# print(f'There are {len(face_locations)} people in this image')
#
# if len(face_locations) == 0:
#     print("no face detected")

str = "imgReg787.png"
num = int(re.findall(r'\d+', str)[0])
print(num/2)