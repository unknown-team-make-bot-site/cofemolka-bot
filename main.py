import telebot
from telebot import types
import config
from models.tables.feedback_table import FeedbackTable
from models.tables.menu_table import MenuTable
import requests
import json

bot = telebot.TeleBot(config.conf['TOKEN'])
feedbacks = FeedbackTable.create_table()
step: str = ""

@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, 'Привет я кофемолка, у меня вы можете ознакомиться с меню '
                                      'и оставить отзыв :)\nПриятного аппетита!')


@bot.message_handler(commands=['start'])
def start_handler(message):
    global step
    # insert_data()
    if (message.chat.id == ""):
        step = "admin"
    else:
        step = "start"
    markup = set_markup(step)
    hello(message)
    bot.send_message(message.chat.id, text='Выберите действие:', reply_markup=markup)

def get_feedbacks_str():
    feedbacks = FeedbackTable.get_feedbacks()
    f_str = "".join([f'{idx + 1}. {f.feedback_text}\n' for idx, f in enumerate(feedbacks)])
    return f_str if f_str else 'Пока что нет отзывов'

@bot.message_handler(regexp="кофе")
def get_coffee(message):
    coffee = get_menu_str()
    bot.send_message(message.chat.id, coffee)
    global step
    step = "coffee"
    markup = set_markup(step)
    bot.send_message(message.chat.id, "Выберите кофе, описание и фотографию которого хотите посмотреть:", reply_markup=markup)
    step = "menu"

def get_menu_str():
    menu = MenuTable.get_dishes()
    f_str = "".join([f'{idx+1}. {m.dish_name}, {m.cost} рублей, {m.volume} мл\n' for idx, m in enumerate(menu)])
    return "Пока что меню пустое" if not menu else f_str

@bot.callback_query_handler(func=lambda call: call.data == 'food_menu')
def menu_ans(call):
    MenuTable.create_table()
    menu = get_menu_str()
    bot.send_message(call.message.chat.id, menu)


@bot.callback_query_handler(func=lambda call: call.data == 'feedback')
def feedback_ans(call):
    result = get_feedbacks_str()
    bot.send_message(call.message.chat.id, result)

@bot.message_handler(regexp = "Меню блюд")
def show_menu(message):
    global step
    step = "menu"
    markup = set_markup(step)
    bot.send_message(message.chat.id,"Выберите категорию:", reply_markup=markup)
    step = "start"

@bot.message_handler(regexp = "Оставить отзыв")
def check_feedback(message):
    global step
    step = "feedback"

@bot.message_handler(func=lambda m: step == "feedback", content_types="text")
def add_feedback(message):
    global step
    FeedbackTable.add_feedback(message.text)
    bot.send_message(message.chat.id, "Спасибо за Ваш отзыв!")
    step = "start"

def set_markup(step):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    if (step == "start"):
        markup.add('Меню блюд', 'Оставить отзыв')
    elif (step == "menu"):
        markup.add("Кофе", "Перекусить", "Десерты", "Другие напитки", "Назад")
    elif (step == "admin"):
        markup.add('Добавить кофе', 'добавить к десертам', 'Добавить к перекусить', "Добавить к напиткам")
    elif (step == "coffee"):
        s = []
        for i in range(1, 12):
            s.append(f"{i}")
            if (i % 4 == 0):
                markup.add(s[0], s[1], s[2], s[3])
                s = []
        markup.add(s[0], s[1], s[2])
        markup.add('Назад')
    return markup

@bot.message_handler(regexp="Назад")
def return_back(message):
    global step
    markup = set_markup(step)
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup = markup)
    if (step == "menu"):
        step = "start"

def insert_data():
    with open('coffee.json', encoding="utf-8", errors="ignore") as json_file:
        data = json.load(json_file)
        for coffee in data:
            MenuTable.add_dishes(coffee['name'], coffee['cost'], type="coffee", volume=coffee['volume'])

# message = bot.get_chat()
bot.polling(none_stop=True)
