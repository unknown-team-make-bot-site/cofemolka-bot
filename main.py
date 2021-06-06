import telebot
import config

bot = telebot.TeleBot(config.conf['TOKEN'])


@bot.message_handlers(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id,'Привет я Cofemolka_bot, у меня вы можете ознакомиться с мееню и оставить отзыв :) Приятного аппетита!')


bot.polling(none_stop=True)
