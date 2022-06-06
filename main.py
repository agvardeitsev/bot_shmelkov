import telebot
from telebot import types
import sqlite3
import datetime
from datetime import date

name = surname = age = ""

day=month=year=0



bot = telebot.TeleBot('5375695745:AAETNH7ETCPxcaESCy6I3HmweyNbd7I3BPY')

connect = sqlite3.connect('users.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users_bot(
    id INTEGER PRIMARY KEY AUTOINCREMENT, id_numb INTEGER, name TEXT, surname TEXT, age INTEGER, day INTEGER, month INTEGER, year INTEGER
)""")
connect.commit()

@bot.message_handler(commands=['start','help'])
def start_message(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    pipl_id = message.chat.id
    cursor.execute(f"SELECT id FROM users_bot WHERE id_numb={pipl_id}")
    data = cursor.fetchone()
    if data is None:
        bot.send_message(message.chat.id, 'Вас приветствует бот-администратор\n ')
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton('регистрация', callback_data='request1')
        item2 = types.InlineKeyboardButton('Инфо', callback_data='request2')
        markup.add(item1, item2)
        bot.send_message(message.chat.id, 'Чем могу помочь ?', reply_markup=markup)
    else:
        cursor.execute(f"SELECT name,surname FROM users_bot WHERE id_numb={pipl_id}")
        bot.send_message(message.chat.id, 'Приветствую '+name+' '+surname)
@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text.lower() == 'да' or message.text.lower() == 'готов':
        bot.send_message(message.from_user.id, 'Здорово, как тебя зовут?')
        bot.register_next_step_handler(message, get_name)

    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю =(... Напиши /help')

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "request1":
        bot.send_message(call.message.chat.id, "Отлично, начинаем регистрацию \nготов ?")
    elif call.data=='request2':
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton('Мне есть 18', callback_data='request1')
        item2 = types.InlineKeyboardButton('Мне нет 18', callback_data='request3')
        markup.add(item1,item2)
        bot.send_message(call.message.chat.id,"ВНИМАНИЕ !!!\nУ данного ресурса есть возрастное ограничение 18+\nПредоставленные данные будут использованы только для работы с ботом", reply_markup=markup)
    elif call.data =='request3':
        bot.send_message(call.message.from_user.id, 'Ваш возраст не удовлетворяет возрастным критериям, /help')

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.chat.id, 'Фамилия ?')
    bot.register_next_step_handler(message, reg_surname)

def reg_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "Год твоего рождения?")
    bot.register_next_step_handler(message, reg_year)

def reg_year(message):
    global year
    while year==0:
        try:
            year= int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, "Ошибка в году, пиши цифрами")
            bot.register_next_step_handler(message, reg_year)
            break
    bot.send_message(message.from_user.id, "Месяц твоего рождения?")
    bot.register_next_step_handler(message, reg_month)

def reg_month(message):
    global month
    while month==0:
        try:
            month=int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, "Ошибка в месяце, пиши цифрами")
            bot.register_next_step_handler(message, reg_month)
            break
    bot.send_message(message.from_user.id, "Число твоего рождения?")
    bot.register_next_step_handler(message, reg_day)

def reg_day(message):
    global day
    while day==0:
        try:
            day=int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, "Ошибка в числе, пиши цифрами")
            bot.register_next_step_handler(message, reg_day)
            break
    bot.send_message(message.from_user.id, "Дата рождения "+str(day)+'.'+str(month)+'.'+str(year)+' , верно ?')
    bot.register_next_step_handler(message, reg_age)

def reg_age(message):
    global age
    td=datetime.datetime.now().date()
    bd = date(int(year), int(month), int(day))
    age= int((td-bd).days/365)
    pipl_id = message.chat.id
    if age<18:
        bot.send_message(message.from_user.id, 'Ваш возраст не удовлетворяет возрастным критериям, /help')
    else:
        cursor.execute("INSERT INTO users_bot(id_numb,name,surname,age,day,month,year) VALUES(?,?,?,?,?,?,?);",(pipl_id, name, surname, int(age),int(day),int(month),int(year)))
        connect.commit()
        bot.send_message(message.from_user.id, "Регистрация прошла успешно\nМожно пользоваться сервисом")
        print ('зарегился '+name+' '+surname)

bot.polling()


