import requests
import json
import face_recognition
import time
from multiprocessing import Process, Pool, Lock, cpu_count
import pickle
from models import Db


def get_attrs(file_name):
    img = face_recognition.load_image_file(file_name)
    face_attrs = face_recognition.face_encodings(img)[0]
    return face_attrs


def view_base():
    for face in Db.get_all_faces():
        print(face.caption + ' ' + str(face.id))


def search_face(face_attrs):
    faces = Db.get_all_faces()
    known_faces_attrs = list([pickle.loads(face.face_attrs) for face in faces])
    results = face_recognition.compare_faces(known_faces_attrs, face_attrs)
    for i, result in enumerate(results):
        if result:
            return faces[i]
    return False


if __name__ == '__main__':
    print(f'starting computations on {cpu_count()} cores')
    lock = Lock()
    start_time = time.time()

    pool = Pool(processes=2)
    #res = pool.map(get_attrs, ("your_file.jpg", "3.jpg"))
    #print(pickle.dumps(res[0]))

    finded = search_face(get_attrs("your_file.jpg"))
    print(finded.caption) if finded else print('Not found')




#        print(pickle.loads(face.face_attrs))

    print("--- %s seconds for 2 ---" % (time.time() - start_time))

#results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
#print(results)