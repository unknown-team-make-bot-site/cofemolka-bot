import telebot
import config

bot = telebot.TeleBot(config.conf['TOKEN'])


@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, 'Привет я Cofemolka_bot, у меня вы можете ознакомиться с мееню и оставить отзыв :)\nПриятного аппетита!')


bot.polling(none_stop=True)
