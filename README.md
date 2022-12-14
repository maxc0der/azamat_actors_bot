
# Установка

 1. Напишите боту @BotFather и создайте бота
 2. Скопируйте токен вида "12345678:AAFIdhW2Kp_EJsal9wVsqyxqAij-YsdSeK0"
 3. Вставьте токен в файл config.py
 4. Конечный вид файла config.py должен быть на подобии:
>  
     token = '12345678:AAFIdhW2Kp_EJsal9wVsqyxqAij-YsdSeK0'
Установим необходимые библиотеки (может занять некоторое время):

      pip install -r requirements.txt
    
    
# Запуск

Запустите файл main.py. После запуска в консоли через несколько секунд  будет выведено "Launched".  Первое распознавание может длиться продолжительное время, так как будут загружены необходимые дата-сеты. 
Если всё установлено штатно, Telegram-bot сразу заработает.
 
# Структура файлов
main.py - основной файл, отвечающий за интеграцию Telegram-бота с системой распознавания.
models.py - скрипт инициализирует локальную базу данных и содержит в себе класс для взаимодействия с ней.
dface.py - скрипт с методами для обнаружения и распознавания лиц.


Дополнительные файлы:
[base_store.py](/) - файл для распознавания лиц из директории и загрузки их в БД
[base_parser_kinoteatr.py](/) - файл для загрузки фото с https://kino-teatr.ru
[base_parser_ruskino.py](/) - файл для загрузки фото с https://ruskino.ru

# Добавление новых актёров

Чтобы загрузить в базу новых актёров, перейдите в base_store.py, и установите путь к папке в формате "name/" и расширение файлов (15-16 строка). 

>   path = 'actors_ruskino_male/'
> 
>   ext = '.jpg'

Папка с фото актёров располагается в корневой директории проекта. В папке имена файлов должны соответсвовать именам актёров.

Далее запустите base_store.py. Через несколько секунд в консоли появится следующий вывод. Число фотографий в папке, прогресс их обработки, и время обработки каждой фотографии. В процессе обработки лица распознаются, и сохраняются в базе данных db.db. После этого они будут доступны для распознавания.
> 3732
> 
> 1 / 3732
> 
> actors_ruskino_male/Абаджян Михаил.jpg
> 
> Time left:  5.115176200866699
> 
> 2 / 3732
> 
> actors_ruskino_male/Абаджян Саят.jpg
> 
> Time left:  5.234664563245432

Далее перейдите в файл dface.py. На 89-ой строчке задаются подстроки, которые должны содержаться в пути к фото, по которым бот осуществляет поиск. (Иными словами - имена папок).
> faces = Db.get_contain_faces('ruskino', 'actors_azamat')

В примере выше поиск осуществляется по папкам, в названиях которых есть "actors_azamat" и "ruskino". То есть, в том числе по папкам "actors_azamat_2", "actors_azamat_3".