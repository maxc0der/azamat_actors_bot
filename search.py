from dface import *
import os

file_name = 'C:/Users/Maxim/Downloads/123.jpg'
faces = get_faces(file_name)
print(faces)

if len(faces) == 0:
    raise 'Faces not founded'

face_path = faces[0]['path']
print(face_path)
print('Exists: ', str(os.path.exists(face_path)))
face = find_face(file_name=face_path)
print(face[0][0].file_name)