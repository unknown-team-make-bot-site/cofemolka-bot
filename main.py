import telebot
from telebot import types
import config
from models.tables.feedback_table import FeedbackTable
from models.tables.menu_table import MenuTable
import requests
import json
import string
import os

bot = telebot.TeleBot(config.conf['TOKEN'])
feedbacks = FeedbackTable.create_table()
step: str = ""
admin: bool = False
@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, 'Привет! Я кофемолка.\n'
                                      'У меня вы можете ознакомиться с меню '
                                      'и оставить отзыв :)\nБодрого кофе!')

@bot.message_handler(commands=['start'])
def start_handler(message):
    global step, admin
    # insert_data()
    if (message.chat.id == config.admins['Daniil']):
        step = "admin"
        admin = True
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
def show_coffee(message):
    coffee = get_coffee()
    bot.send_message(message.chat.id, coffee)
    global step
    step = "coffee"
    markup = set_markup(step)
    bot.send_message(message.chat.id, "Выберите кофе, описание и фотографию которого хотите посмотреть:", reply_markup=markup)
    step = "coffee_products"

def get_dishes():
    menu = MenuTable.get_dishes()
    m_str = "".join([f'{idx+1}. {m.dish_name}, {m.cost} рублей, {m.volume} мл\n' for idx, m in enumerate(menu)])
    return "Пока что меню пустое" if not menu else m_str

def get_dishes_with_type(type):
    menu = MenuTable.get_type(type)
    if (type == "coffee"):
        # return coffee
    if (type == "snacks"):
        # return snacks
@bot.message_handler(regexp="Посмотреть отзывы")
def show_feedbacks(message):
    feedbacks = get_feedbacks()
    bot.send_message(message.chat.id, feedbacks)

def get_feedbacks():
    feedbacks = FeedbackTable.get_feedbacks()
    f_str = "".join(f'{idx+1}. {f.feedback_text}\n' for idx, f in enumerate(feedbacks))
    return "Пока что не отзывов" if not feedbacks else f_str

'''

Как это работает? 

@bot.callback_query_handler(func=lambda call: call.data == 'food_menu')
def menu_ans(call):
    MenuTable.create_table()
    menu = get_menu_str()
    bot.send_message(call.message.chat.id, menu)

@bot.callback_query_handler(func=lambda call: call.data == 'feedback')
def feedback_ans(call):
    result = get_feedbacks_str()
    bot.send_message(call.message.chat.id, result)
'''

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

@bot.message_handler(regexp="Панель админа")
def back_to_admin(message):
    markup = set_markup("admin")
    bot.send_message(message.chat.id, text="Приветствуем админа!", reply_markup=markup)

@bot.message_handler(regexp="Посмотреть бота")
def back_to_bot(message):
    markup = set_markup("start")
    bot.send_message(message.chat.id,text="Приветствуем админа!", reply_markup=markup)

@bot.message_handler(regexp="Перекусить")
def show_snacks(message):
    global step
    step = "snacks"
    snacks = get_menu_str(step)
    markup = set_markup(step)

def set_markup(step):
    global admin
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    emj = config.emojis
    if (step == "start"):
        markup.add(emj['Меню'] + 'Меню блюд', emj['Отзыв'] + 'Оставить отзыв')
        if (admin == True):
            markup.add("Панель админа")
    elif (step == "menu" or step == "coffee_products"):
        markup.add(emj['Кофе'] + "Кофе", emj['Закуски'] + "Перекусить")
        markup.add(emj['Десерты'] + "Десерты",
                   emj['Напитки'] + "Другие напитки")
        markup.add(emj['Назад'] + "Назад")
    elif (step == "admin"):
        markup.add('Посмотреть отзывы')
        markup.add('Добавить кофе', 'добавить к десертам')
        markup.add('Добавить к перекусить', "Добавить к напиткам")
        markup.add('Посмотреть бота')
    # set 1 to 11 buttons on step products coffee
    elif (step == "coffee"):
        s = []
        for i in range(1, 12):
            s.append(f"{i}")
            if (i % 4 == 0):
                markup.add(s[0], s[1], s[2], s[3])
                s = []
        markup.add(s[0], s[1], s[2])
        markup.add(emj['Назад'] + 'Назад')
    elif (step == "snacks"):
        markup.add("1", "2")
        markup.add("Назад")
    return markup

@bot.message_handler(regexp="Назад")
def return_back(message):
    global step
    markup = set_markup(step)
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup = markup)
    if (step == "menu" or step == "coffee_products"):
        step = "start"


def insert_data():
    with open('data/coffee.json', encoding="utf-8", errors="ignore") as json_file:
        data = json.load(json_file)
        for coffee in data:
            MenuTable.add_dishes(coffee['name'], coffee['cost'], type="coffee", volume=coffee['volume'],
                                 description=coffee['description'], image=coffee['image'])
    with open('data/eat_something.json', encoding="utf-8", errors="ignore") as json_file:
        data = json.load(json_file)
        for food in data:
            MenuTable.add_dishes(food['name'], food['cost'], type="snacks",
                                 description=food['description'], image=food['image'])


@bot.message_handler(content_types=['text'])
def process_digit_buttons(message):
    global step
    product_number = message.text.isdigit()
    if (product_number and step == "coffee_products"):
        product_number = message.text
        coffee = MenuTable.get_dishes()
        for idx, el in enumerate(coffee):
            if (product_number == str(idx)):
                bot.send_message(message.chat.id, el.description)
                bot.send_photo(message.chat.id, photo=open(el.image, 'rb'))

bot.polling(none_stop=True)


# if visualise photo will be on client-side, for example photo on server and need download the same into pc or phone
def writeToFile(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

def readBlobData(photo):
    photoPath = os.getcwd() + photo + ".jpg"
    writeToFile(photo, photoPath)

'''
Okay, so i need to send
    description and image when
        user clicked to text that is digit 
        
if message.text.isdigit() then 
    check current step
    if step is coffee (or any other dish) then
        
            getCoffeeFromDb("SELECT * from dish where type = "coffee")
            get_menu_str() ==> dishes
            for (el in dishes)
            id array element in array
            for (el, idx in enumerate(array))
                if message.text.digit == idx then
                    send coffee[message.text.digit][description] && coffee[message.text.digit][image]
                    
Problem 1:
1. add content to menu 
'''
