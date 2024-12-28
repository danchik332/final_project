from config import TOKEN
import telebot
from telebot import types
import sqlite3
import random
#Импортирование библиотек

bot = telebot.TeleBot(TOKEN)

# Подключаемся к базе данных
connection = sqlite3.connect('career_advisor.db', check_same_thread=False)
cursor = connection.cursor()

# Создание таблицы, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS careers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profession TEXT NOT NULL,
    description TEXT NOT NULL
)
''')

# Данные для добавления
careers = [
    ("Программист", "Специалист по разработке программного обеспечения."),
    ("Дизайнер", "Профессионал, занимающийся созданием визуального контента."),
    ("Аналитик данных", "Эксперт по анализу и интерпретации данных."),
    ("Менеджер проектов", "Профессионал, осуществляющий планирование и контроль проектов."),
    ("Маркетолог", "Специалист по разработке и реализации маркетинговых стратегий."),
    ("Инженер-строитель", "Эксперт в области проектирования и строительства зданий.")
]

# Вставляем данные в таблицу
cursor.executemany('''
INSERT INTO careers (profession, description)
VALUES (?, ?)
''', careers)

connection.commit()

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я бот-Советчик по выбору карьеры. Чем могу помочь?")
    main_menu(message.chat.id)

    

def main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Получить совет")
    item2 = types.KeyboardButton("Справка")
    markup.add(item1, item2)
    bot.send_message(chat_id, "Выберите опцию:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Получить совет")
def get_advice(message):
    cursor.execute("SELECT profession, description FROM careers")
    careers = cursor.fetchall()
    chosen_career = random.choice(careers)
    
    response = f"Профессия: {chosen_career[0]} Описание: {chosen_career[1]}"
    bot.send_message(message.chat.id, response)
    main_menu(message.chat.id)

    

@bot.message_handler(func=lambda message: message.text == "Справка")
def help_command(message):
    bot.send_message(message.chat.id, "Это бот, который поможет вам выбрать карьерный путь. Вы можете получить случайные советы по профессиям.")
    main_menu(message.chat.id)

def add_career(profession, description):
    cursor.execute("INSERT INTO careers (profession, description) VALUES (?, ?)", (profession, description))
    connection.commit()

if __name__ == "__main__":
    bot.polling(none_stop=True)