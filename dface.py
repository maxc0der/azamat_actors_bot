from deepface import DeepFace
from deepface.commons import functions, distance as dst
from retinaface import RetinaFace
import time
import cv2
from models import Db, Face
from random import randint
import pickle


models = ['Facenet512', 'VGG-Face', 'SFace', 'OpenFace', 'DeepFace', 'DeepID', 'Dlib']
model = DeepFace.build_model(models[0])
target_size = model.layers[0].input_shape
print(target_size)


def get_vector(file_path):
    #preprocess = functions.preprocess_face(file_path, target_size=[target_size[0][1], target_size[0][2]])
    #vector = model.predict(preprocess)
    vector = DeepFace.represent(img_path=file_path, model_name=models[0], enforce_detection=False)
#    obj = DeepFace.analyze(img_path=file_path, actions=['age', 'gender'], enforce_detection=False)
#    print(obj)
    return vector


def compare_vectors(v1, v2):
    distance = dst.findCosineDistance(v1, v2)
    threshold = dst.findThreshold(model, 'cosine')
    return distance
    #if distance <= threshold:
    #    return distance
    #else:
    #    return False


def get_faces(file_name):
    paths = list()
    img = cv2.imread(file_name)
    faces = RetinaFace.detect_faces(img, threshold=0.3, allow_upscaling=True)
    if 'face_1' not in faces:
        return list()

    areas = list()
    for i in faces.keys():
        choose = faces[i]
        area = choose['facial_area']
        areas.append(area)

    areas.sort(key=lambda x: x[0])
    print(areas)

    for i, area in enumerate(areas):
        random_number = randint(100000, 999999)
        path = 'images/' + str(random_number) + '_' + str(i) + '.jpeg'
        cv2.imwrite(path, img[area[1]:area[3], area[0]:area[2]])
        #img = cv2.rectangle(img, (area[0], area[1]),  (area[2], area[3]), (0, 255, 0), 2)
        point1, point2 = (area[0], area[1]), (area[2], area[3])
        paths.append({'path': path, 'p1': point1, 'p2': point2})
    cv2.imwrite(file_name, img)
    return paths


def find_face(file_name=None, vector=None):
    results = list()
    yo = get_yo(file_name)
    print(yo)

    if vector is None:
        vector = get_vector(file_name)
    faces = Db.get_all_faces()
    #faces = Db.get_contain_faces('')
    for face in faces:
        known_vector = pickle.loads(face.face_attrs)
        distance = compare_vectors(known_vector, vector)
        if distance and abs(face.age - yo['age']) <= 7:
            results.append([face, distance])
    if len(results) > 0:
        sorted_results = sorted(results, key=lambda x: x[1])
        return [[sorted_results[0][0], sorted_results[0][1]],
                [sorted_results[1][0], sorted_results[1][1]],
                [sorted_results[2][0], sorted_results[2][1]]]
    return None


def store_face(file_name=None, vector=None, caption=None, db_file_name=None):
    if vector is None:
        vector = get_vector(file_name)
  ##  if find_face(vector=vector) is None:
    if db_file_name is not None:
        Db.store_face(db_file_name, caption, vector)
    else:
        Db.store_face(file_name, caption, vector)


def get_yo(file_name):
    obj = DeepFace.analyze(img_path=file_name, actions=['age'], enforce_detection=False)
    age = obj['age']
    return {'age': age}


def store_yo(file_name=None, db_file_name=None):
    yo = get_yo(file_name)
    print(yo)
    Db.update(db_file_name, yo['age'])

    #    return True  # OK
  #  else:
   #     return False  # Already exists

