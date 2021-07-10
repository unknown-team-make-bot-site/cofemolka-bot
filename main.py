import telebot
from telebot import types
import config
from models.tables.feedback_table import FeedbackTable
from models.tables.menu_table import MenuTable

bot = telebot.TeleBot(config.conf['TOKEN'])


@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, 'Привет я кофемолка, у меня вы можете ознакомиться с меню '
                                      'и оставить отзыв :)\nПриятного аппетита!')


@bot.message_handler(commands=['start'])
def menu(message):
    markup = types.InlineKeyboardMarkup()
    menu_btn = types.InlineKeyboardButton(text='Меню блюд', callback_data='food_menu')
    send_feedback_btn = types.InlineKeyboardButton(text='Оставить отзыв', callback_data='feedback')
    markup.add(menu_btn, send_feedback_btn)
    hello(message)
    bot.send_message(message.chat.id, text='Выберите действие:', reply_markup=markup)


def get_feedbacks_str():
    feedbacks = FeedbackTable.get_feedbacks()
    f_str = "".join([f'{idx + 1}. {f.feedback_text}\n' for idx, f in enumerate(feedbacks)])
    return f_str if f_str else 'Пока что нет отзывов'


def get_menu_str():
    menu = MenuTable.get_dishes()
    return "Пока что меню пустое" if not menu else menu


@bot.callback_query_handler(func=lambda call: call.data == 'food_menu')
def menu_ans(call):
    menu = get_menu_str()
    bot.send_message(call.message.chat.id, menu)


@bot.callback_query_handler(func=lambda call: call.data == 'feedback')
def feedback_ans(call):
    FeedbackTable.create_table()
    result = get_feedbacks_str()
    bot.send_message(call.message.chat.id, result)


bot.polling(none_stop=True)
