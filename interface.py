import telebot
from telebot import types
import config
from models.tables.menu_table import MenuTable

dish_types = {
    "coffee": 1,
    "eat_something": 2,
    "deserts": 3,
    "tea": 4,
    "milkshakes": 5,
    "other": 6
}

def add_inline_markup(number):
    remains = [0,1, 2, 3]
    markup = types.InlineKeyboardMarkup(row_width=4)
    if (number >= 4 and (number % 4) in remains):
        markup = add_inline_buttons(number, 4, markup)
    elif (number >= 3 and number % 3 in remains):
        markup = add_inline_buttons(number, 3, markup)
    elif (number >= 2 and number % 2 in remains):
        markup = add_inline_buttons(number, 2, markup)
    elif (number == 1):
        markup = markup.add(1, callback_data = 1)
    return markup

def add_inline_buttons(number, divider, markup):
    b = []
    inline_buttons = []
    for i in range(1,number + 1):
        b.append(i)
        if (i % divider == 0 and i != 0):
            for j in range(0, divider):
                inline_buttons.append(types.InlineKeyboardButton(text = b[j], callback_data = b[j]))
            if (divider == 4):
                markup.add(inline_buttons[0], inline_buttons[1], inline_buttons[2], inline_buttons[3])
            elif (divider == 3):
                markup.add(inline_buttons[0], inline_buttons[1], inline_buttons[2])
            elif (divider == 2):
                markup.add(inline_buttons[0], inline_buttons[1])
            b = []
            inline_buttons = []
    for i in range(0, len(b)):
        inline_buttons.append(types.InlineKeyboardButton(text = b[i], callback_data = b[i]))
    if (len(b) == 4):
        markup.add(inline_buttons[0], inline_buttons[1], inline_buttons[2], inline_buttons[3])
    elif (len(b) == 3):
        markup.add(inline_buttons[0], inline_buttons[1], inline_buttons[2])
    elif (len(b) == 2):
        markup.add(inline_buttons[0], inline_buttons[1])
    return markup

def get_count_dishes(type_id):
    count = MenuTable.get_count_dishes(type_id)
    return count[0][0]


markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
emj = config.emojis

start = types.ReplyKeyboardMarkup(resize_keyboard=True)
start.add(emj['Меню'] + 'Меню блюд', emj['Отзыв'] + 'Оставить отзыв')

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(emj['Кофе'] + "Кофе", emj['Закуски'] + "Перекусить")
menu.add(emj['Десерты'] + "Десерты",emj['Напитки'] + "Другие напитки")
menu.add("Чай", "Молочные коктейли")
menu.add(emj['Назад'] + "Назад")

start_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
# start.add(emj['Меню'] + 'Меню блюд', emj['Отзыв'] + 'Оставить отзыв')


admin_view = types.ReplyKeyboardMarkup(resize_keyboard=True)
admin_view.add('Посмотреть отзывы')
admin_view.add('Добавить кофе', 'добавить к десертам')
admin_view.add('Добавить к перекусить', "Добавить к напиткам")
admin_view.add('Посмотреть бота')


coffee = add_inline_markup(get_count_dishes(dish_types["coffee"]))
deserts = add_inline_markup(get_count_dishes(dish_types["deserts"]))
snacks = add_inline_markup(get_count_dishes(dish_types["eat_something"]))
tea = add_inline_markup(get_count_dishes(dish_types["tea"]))
milkshakes = add_inline_markup(get_count_dishes(dish_types["milkshakes"]))
other = add_inline_markup(get_count_dishes(dish_types["other"]))
