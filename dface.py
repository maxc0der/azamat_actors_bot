"""
Модуль работы с лицами.
get_vector(file_path) -> vector
compare_vectors(v1, v2) -> distance
get_faces(file_name) -> paths [list of {'path': path, 'p1': point1, 'p2': point2}]
find_face(file_name=None, vector=None, max_age_distance=7) -> [[face, distance], [face, distance], [face, distance]]
store_face(file_name=None, vector=None, caption=None, db_file_name=None)
get_yo(file_name) -> age (int)
store_yo(file_name=None, db_file_name=None)
"""

from deepface import DeepFace
from deepface.commons import distance as dst
from retinaface import RetinaFace
import cv2
from models import Db, Face
from random import randint
import pickle


models = ['Facenet512', 'VGG-Face', 'SFace', 'OpenFace', 'DeepFace', 'DeepID', 'Dlib']
model = DeepFace.build_model(models[0])
target_size = model.layers[0].input_shape
print(target_size)


def get_vector(file_path):
    """ Функция распознает лицо и возвращает вектор """
    #preprocess = functions.preprocess_face(file_path, target_size=[target_size[0][1], target_size[0][2]])
    #vector = model.predict(preprocess)
    vector = DeepFace.represent(img_path=file_path, model_name=models[0], enforce_detection=False)
#    obj = DeepFace.analyze(img_path=file_path, actions=['age', 'gender'], enforce_detection=False)
#    print(obj)
    return vector


def compare_vectors(v1, v2):
    """Возвращает разницу между двумя векторами лиц (расхождение)"""
    distance = dst.findCosineDistance(v1, v2)
    threshold = dst.findThreshold(model, 'cosine')
    return distance


def get_faces(file_name):
    """Обнаруживает все лица на фото, сохраняет их с индексами _0, _1, _2 и.т.д \n
    возвращает список словарей формата {'path': path, 'p1': point1, 'p2': point2}"""
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


def find_face(file_name=None, vector=None, max_age_distance=7):
    """**Функция поиска лиц на фото.** \n
    Если лица найдены - возвращает список [лицо, расхождение] для трёх наиболее похожих лиц \n
    **max_age_distance** - максимальный модуль разницы возрастов \n
    **vector** [опционально] - вектор лица \n
    **file_name** [опционально] - путь к изображению для распознавания \n
    Аргументы должны содержать либо vector, либо file_name"""
    results = list()
    yo = get_yo(file_name)
    print(yo)

    if vector is None:
        vector = get_vector(file_name)
    #faces = Db.get_all_faces()

    # ФИЛЬТРЫ ПО ПАПКАМ
    faces = Db.get_contain_faces('ruskino', 'actors_azamat')
    for face in faces:
        known_vector = pickle.loads(face.face_attrs)
        distance = compare_vectors(known_vector, vector)
        if distance and abs(face.age - yo) <= max_age_distance:
            results.append([face, distance])
    if len(results) > 0:
        sorted_results = sorted(results, key=lambda x: x[1])
        return [[sorted_results[0][0], sorted_results[0][1]],
                [sorted_results[1][0], sorted_results[1][1]],
                [sorted_results[2][0], sorted_results[2][1]]]
    return None


def store_face(file_name=None, vector=None, caption=None, db_file_name=None):
    """**Записывает лицо в базу данных.** \n
    Может принимать как уже распознанное лицо (вектор), так и путь к изображению для распознавания. \n
    **vector** [опционально] - вектор лица \n
    **file_name** [опционально] - путь к изображению для распознавания \n
    *Аргументы должны содержать либо vector, либо file_name* \n
    **caption** - описание лица (например имя фамилия)"""
    if vector is None:
        vector = get_vector(file_name)
    if db_file_name is not None:
        Db.store_face(db_file_name, caption, vector)
    else:
        Db.store_face(file_name, caption, vector)


def get_yo(file_name):
    """Функция для определения возраста по фото"""
    obj = DeepFace.analyze(img_path=file_name, actions=['age'], enforce_detection=False)
    return obj['age']


def store_yo(file_name=None, db_file_name=None):
    """**Функция для добавления возраста в базу данных** \n
    **file_name** - путь к изображению \n
    **db_file_name** - имя файла в базе данных (критерий поиска)"""
    yo = get_yo(file_name)
    print(yo)
    Db.update(db_file_name, yo)

