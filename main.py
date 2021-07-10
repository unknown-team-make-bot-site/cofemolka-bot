import telebot
from telebot import types
import config
from models.tables.feedback_table import FeedbackTable

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


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    result = ''
    if call.data == 'food_menu':
        feedbacks = FeedbackTable.get_feedbacks()
        result = '1.\n 2.\n 3.'
    elif call.data == 'feedback':
        result = 'Оставьте отзыв:'
        FeedbackTable.create_table()
    bot.send_message(call.message.chat.id, result)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


bot.polling(none_stop=True)
