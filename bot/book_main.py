import telebot
from telebot import types
import json
import datetime
import sqlite3
bot = telebot.TeleBot('6424586882:AAGyo9-S9XcxITCOgScrf2_YCZoc3IR-09Q')

ERROR_TEXT = "Произошла ошибка, попробуйте ещё раз или обратитесь к администратору"
DEBUG = False  # TODO debug == true - идёт разработка

#TODO Таблица






def decorator_exception_1(func):
    def wrapper(*args, **kwargs):
        message: telebot.types.Message = args[0]
        try:
            func(*args, **kwargs)
        except Exception as error:
            _error = f"error: {error}"
            print(_error)
            with open("logs/errors.txt", mode="a", encoding="utf-8") as file:
                file.write(f"[{datetime.datetime.now()}] {error}\n")
            if DEBUG:
                bot.send_message(message.chat.id, _error, parse_mode='html')
            else:
                bot.send_message(message.chat.id, ERROR_TEXT, parse_mode='html')

    return wrapper


@decorator_exception_1
@bot.message_handler(commands=['start'])
def b_start(message):
    commands = """
    <strong>Привет! Я бот специализуюванный на публикации книг</strong>

    <b>Ниже список команд с описанием:</b>

    <i>Базовые</i>
    /start - начальное меню

    <i>Публикация книг</i>
    /publish - Публикация твоей новой книги
    
    <i>Список книг</i>
    /list - Список всех опубликованный книг
    """


    markup = types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, commands, parse_mode='html', reply_markup=markup)


@decorator_exception_1
@bot.message_handler(commands=['publish'])
def b_publish(message):
    bot.send_message(message.chat.id,
                     """<b>Введите через запятую название книги,жанр книги,цена книги и имя автора: """)
    bot.register_next_step_handler(message, b_book)


def b_book(message: telebot.types.Message):
    data = message.text.split(",")

    title: str = data[0].strip().capitalize()
    genre: str = data[1].strip()
    price: float = float(data[2].strip())
    name: str = data[3].strip().capitalize()
    # print(title, count, price)

    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()


    cursor.execute(f'INSERT INTO books (title, genre, price, name) VALUES 'f"('{title}', '{genre}', '{price}', '{name}');")
    conn.commit()
    conn.close()

@decorator_exception_1
@bot.message_handler(commands=['list'])
def b_list(message):
    bot.send_message(message.chat.id,"<b>Вот список книг:</b>\n\n")
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")


    rows = cursor.fetchall()


    for row in rows:
        id = row[0]
        title = row[1]
        genre = row[2]
        price = row[3]
        name = row[4]


        bot.send_message(message.chat.id,f'Title: {title},\nGenre: {genre},\nPrice: {price}, \nName: {name}\n')


    conn.close()





if __name__ == "__main__":
    print("bot started...")
    try:
        bot.infinity_polling()
    except Exception as error:
        print("error: ", error)
    print("bot stopped...")