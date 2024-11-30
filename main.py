import telebot
import webbrowser
from telebot import types
import sqlite3

bot = telebot.TeleBot('8080715864:AAG0geyPToXRtmy5JxSv_BL-RixBwrfByfY')

#----Старт----#
@bot.message_handler(commands=['start'])
def main(message):
    
    #----БД----#
    conn = sqlite3.connect('db.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    #----Кнопки (быстрый ответ)----#
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Открыть сайт')
    btn2 = types.KeyboardButton('Удалить')
    btn3 = types.KeyboardButton('куку')
    markup.row(btn1, btn2, btn3)

    #----Отправить файл----#
    #file = open('./photo.jpeg', 'rb')
    #bot.send_photo(message.chat.id, file, reply_markup=markup)
    #bot.send_audio(message.chat.id, file, reply_markup=markup)
    #bot.send_video(message.chat.id, file, reply_markup=markup)

    #----Отправить сообщение и ждать ответ----#
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

#----Обработать ответ----#
def on_click(message):
    if message.text == 'Открыть сайт':
        bot.send_message(message.chat.id, 'Открыт')
    elif message.text == 'Удалить':
        bot.send_message(message.chat.id, 'Удал')

#----Команды----#
@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>Help</b> <em>info</em>', parse_mode='html')

#----Обработка сообщений----#
@bot.message_handler()
def main(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    elif message.text.lower() == 'куку':
        #----Кнопки в ответе----#
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Открыть сайт', url='http://192.168.0.113:5173')
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton('Удалить ответ', callback_data='delete')
        btn3 = types.InlineKeyboardButton('Изменить ответ', callback_data='edit')
        btn4 = types.InlineKeyboardButton('Удалить сообщ', callback_data='delete_prev')
        markup.row(btn2, btn3, btn4)
        bot.reply_to(message, 'Привет', reply_markup=markup )
#----Обработка кнопок в ответе----#
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'delete_prev':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)

#----Открыть сайт (бот)----
#@bot.message_handler(commands=['site'])
#def main(message):
#    webbrowser.open('https://google.com')

bot.polling(none_stop=True)