import face_recognition

# image_of_bill = face_recognition.load_image_file('./img/known/Bill Gates.jpg')
# bill_face_encoding = face_recognition.face_encodings(image_of_bill)[0]
#
# unknown_image = face_recognition.load_image_file(
#     './img/unknown/noface.png')
# unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
# # Compare faces
# results = face_recognition.compare_faces(
#     [bill_face_encoding], unknown_face_encoding)
#
# if results[0]:
#     print('This is Bill Gates')
# else:
#     print('This is NOT Bill Gates')
try:
    image_of_bill = face_recognition.load_image_file('./imgRecord.png')
    bill_face_encoding = face_recognition.face_encodings(image_of_bill)[0]

    unknown_image = face_recognition.load_image_file(
        './students/ResizedAniebiet100.png')
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

    # Compare faces
    results = face_recognition.compare_faces(
        [bill_face_encoding], unknown_face_encoding)

    if results[0]:
        print('This is Aniebiet')
    else:
        print('This is not Aniebiet')
except:
    print("no face found")
