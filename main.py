import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.conf['TOKEN'])


@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, 'Привет я Cofeemolka_bot, у меня вы можете ознакомиться с мееню '
                                      'и оставить отзыв :)\nПриятного аппетита!')



@bot.message_handler(commands=['start'])
def menu(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Меню блюд епт', callback_data='food_menu'))
    markup.add(telebot.types.InlineKeyboardButton(text='Оставить отзыв', callback_data='feedback'))
    bot.send_message(message.chat.id, 'Привет я Cofemolka_bot, у меня вы можете ознакомиться с мееню и оставить отзыв :)\nПриятного аппетита!')
    bot.send_message(message.chat.id, text='Выберете дейтвие:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    result = ''
    if call.data == 'food_menu':
        result = '1.\n 2.\n 3.'
    elif call.data == 'feedback':
        result = 'Оставьте отзыв:'
    bot.send_message(call.message.chat.id, result)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
bot.polling(none_stop=True)
