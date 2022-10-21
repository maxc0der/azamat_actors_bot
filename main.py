from dface import *
import telebot
import config
import cv2
from telebot import types
from models import Db, Face
import urllib.parse


def draw_rectangles(file_name, faces):
    img = cv2.imread(file_name)
    for face in faces:
        img = cv2.rectangle(img, face['p1'], face['p2'], face['color'], 3)
    cv2.imwrite(file_name, img)


print('Launched')
bot = telebot.TeleBot(config.token)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    print(call)
    chat_id = call.message.chat.id
    if 'id' in call.data:
        id = call.data[2:]
        face = Db.get_face(int(id))
        caption = '✅ ' + face.caption
        bot.send_photo(chat_id, open(face.file_name, 'rb'), caption=caption)
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Success")


@bot.message_handler(content_types=["text", "photo"])
def repeat_all_messages(message):
    chat_id = message.chat.id
    text = message.text
    if message.content_type == 'photo':
        bot.send_message(chat_id, '⬇ Загрузка фото, ожидайте...')
        raw = message.photo[-1].file_id
        file_name = "images/" + raw + ".jpg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        result = list()
        faces = get_faces(file_name)
        #for i, item in enumerate(faces):
        face = find_face(file_name=faces[0]['path'])

#            result.append(str(i + 1) + ': ' + '💬 Лицо не знакомо')
 #           faces[i]['color'] = (0, 0, 255)
        if face is not None:
            first_face = face[0][0]
            second_face = face[1][0]
            third_face = face[2][0]

        if len(faces) > 0:
            print('Count: ', str(len(faces)))
            if message.caption is not None:
                store_face(file_name=faces[0]['path'], caption=message.caption)
                bot.send_message(chat_id, '✅ Фото загружено')
            else:
                bot.send_message(chat_id, '⏳ Фото загружено, распознаём...')


                #        result.append(str(i + 1) + ': ✅ ' + face.caption)
                #        faces[i]['color'] = (0, 255, 0)
                #draw_rectangles(file_name, faces)
                #bot.send_photo(chat_id, open(file_name, 'rb'), caption='\n'.join(result))
                caption = '✅ ' + first_face.caption
                caption = caption + '\n\nДругие варианты:\n'
                caption = caption + '- ' + second_face.caption + '\n'
                caption = caption + '- ' + third_face.caption

                keyboard = types.InlineKeyboardMarkup()
                s1 = types.InlineKeyboardButton(text='🔍 Google', url='https://www.google.com/search?q=' + urllib.parse.quote(first_face.caption))
                s2 = types.InlineKeyboardButton(text='🔍 Yandex', url='https://yandex.ru/search/?text=' + urllib.parse.quote(first_face.caption))
                b1 = types.InlineKeyboardButton(text=second_face.caption, callback_data='id' + str(second_face.id))
                b2 = types.InlineKeyboardButton(text=third_face.caption, callback_data='id' + str(third_face.id))
                keyboard.row(s1, s2)
                keyboard.add(b1)
                keyboard.add(b2)

                bot.send_photo(chat_id, open(first_face.file_name, 'rb'), caption=caption, reply_markup=keyboard)
        else:
            bot.send_message(chat_id, '⚠️ На фото не обнаружены лица')
    #bot.send_message(chat_id, message.text)


bot.infinity_polling()


