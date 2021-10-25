import telebot
from telebot import types
import config
import interface
from interface import coffee, snacks, other, tea, milkshakes, menu, admin_view, deserts
from models.tables.feedback_table import FeedbackTable
from models.tables.menu_table import MenuTable
import os


bot = telebot.TeleBot(config.conf['TOKEN'])
step: str = ""
admin: bool = False

dish_types = {
    "coffee": 1,
    "eat_something": 2,
    "deserts": 3,
    "tea": 4,
    "milkshakes": 5,
    "other": 6
}

@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, 'Привет! Я кофемолка.\n'
                                      'У меня вы можете ознакомиться с меню '
                                      'и оставить отзыв :)\nБодрого кофе!')

@bot.message_handler(commands=['start'])
def start_handler(message):
    global step, admin
    # insert_data()
    if (message.chat.id in config.admins.values()):
        admin = True
        interface.start.add("Панель админа")
    hello(message)
    bot.send_message(message.chat.id, text='Выберите действие:', reply_markup=interface.start)

def get_feedbacks_str():
    feedbacks = FeedbackTable.get_feedbacks()
    f_str = "".join([f'{idx + 1}. {f.feedback_text}\n' for idx, f in enumerate(feedbacks)])
    return f_str if f_str else 'Пока что нет отзывов'

@bot.message_handler(commands=["Кофе"])
def show_coffee(message):
    global step
    step = "coffee"
    text = get_dishes_with_type(step)
    bot.send_message(message.chat.id, text,reply_markup=coffee)

@bot.message_handler(regexp="Перекусить")
def show_snacks(message):
    global step
    step = "eat_something"
    text = get_dishes_with_type(step)
    bot.send_message(message.chat.id, text, reply_markup = snacks)

@bot.message_handler(regexp="Десерты")
def show_deserts(message):
    global step
    step = "deserts"
    text = get_dishes_with_type(step)
    bot.send_message(message.chat.id, text,reply_markup=deserts)

@bot.message_handler(regexp="Назад")
def back(message):
    bot.send_message(message.chat.id, text="Выберите категорию:", reply_markup=interface.start)

@bot.message_handler(regexp="Другие напитки")
def show_other(message):
    global step
    step = "other"
    text = get_dishes_with_type(step)
    bot.send_message(message.chat.id, text,reply_markup=other)

@bot.message_handler(regexp="Чай")
def show_tea(message):
    global step
    step = "tea"
    text = get_dishes_with_type(step)
    bot.send_message(message.chat.id, text,reply_markup=tea)

@bot.message_handler(regexp="Молочные коктейли")
def show_milkshakes(message):
    global step
    step = "milkshakes"
    text = get_dishes_with_type(step)
    bot.send_message(message.chat.id, text,reply_markup=milkshakes)

def get_dishes():
    menu = MenuTable.get_dishes()
    m_str = "".join([f'{idx+1}. {m.dish_name}, {m.cost} рублей, {m.volume} мл\n' for idx, m in enumerate(menu)])
    return "Пока что меню пустое" if not menu else m_str

def get_dishes_with_type(type):
    if (type in dish_types.keys()):
        type_id = dish_types[type]
        dishes = MenuTable.get_dishes_with_type(type_id)
        if (type == "eat_something" or type == "deserts"):
            d_str = "".join(f"{idx + 1}. {d.dish_name} {d.cost} Р \n" for idx, d in enumerate(dishes))
        else:
            d_str = "".join(f"{idx + 1}. {d.dish_name} {d.cost} Р {d.volume} мл \n" for idx, d in enumerate(dishes))
        return d_str

@bot.message_handler(regexp="Посмотреть отзывы")
def show_feedbacks(message):
    feedbacks = get_feedbacks()
    bot.send_message(message.chat.id, feedbacks)

def get_feedbacks():
    feedbacks = FeedbackTable.get_feedbacks()
    f_str = "".join(f'{idx+1}. {f.feedback_text}\n' for idx, f in enumerate(feedbacks))
    return "Пока что не отзывов" if not feedbacks else f_str

@bot.message_handler(regexp = "Меню блюд")
def show_menu(message):
    bot.send_message(message.chat.id,"Выберите категорию:", reply_markup=menu)

@bot.message_handler(regexp = "Оставить отзыв")
def add_feedback(message):
    global step
    step = "feedback"

@bot.message_handler(func=lambda x: step == "feedback", content_types="text")
def thanks_to_user(message):
    global step
    FeedbackTable.add_feedback(message.text)
    bot.send_message(message.chat.id, "Спасибо за Ваш отзыв!")
    step = "start"

@bot.message_handler(regexp="Панель админа")
def back_to_admin(message):
    bot.send_message(message.chat.id, text="Приветствуем админа!", reply_markup=admin_view)

@bot.message_handler(regexp="Посмотреть бота")
def back_to_bot(message):
    bot.send_message(message.chat.id, text="Приветствуем админа!", reply_markup=interface.start)

@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def process_digit_buttons(call):
    global step
    coffee = MenuTable.get_dishes_with_type(dish_types[step])
    for idx, el in enumerate(coffee):
        if (call.data == str(idx + 1)):
            bot.send_photo(call.message.chat.id, photo=open(f"product_images/{step}/{el.image}", 'rb'), caption=el.description)

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
1. add content to menu V
2. markup in main file is excess, need to create new file with other MORE comfortable structure 

then if else branching 

content // complete
need to insert data // complete
admin panel should be working, how to check if admin user or not?
created buttons prevent reading main chat-bot logic, so it needed to add in other file
feedback button is not working, so it is immediately send "thanks": // complete 
    1. user clicked on feedback button
    2. type something
    3. Thanks for user! 
'''
