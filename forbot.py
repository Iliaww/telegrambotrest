import telebot
import re


from telebot import types
from string import Template
#botapi
bot = telebot.TeleBot('5141130196:AAF3z5H6eUafLkV52HXll8iLbntdgZrLA2I')


user_dict = {}


class User:
    def __init__(self, city):
        self.city = city

        keys = ['fullname', 'phone', 'driverSeria', 
                'driverNumber', 'driverDate', 'car', 
                'carModel', 'carColor', 'carNumber', 'carDate']
        
        for key in keys:
            self.key = None

print(bot.get_me())
#userchatid
user_2 = 916571248  # id: int
#/start
@bot.message_handler(commands=["start"])

def start(message):

#keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Оставить отзыв")
    item2 = types.KeyboardButton("Информация")
    item3 = types.KeyboardButton("Бронь")
    item4 = types.KeyboardButton("Подозвать официанта")
#add items to markup
    markup.add(item1, item2, item3, item4)
#helloex
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>,\nБот-отзовик.".format(message.from_user, bot.get_me()),
        parse_mode = 'html', reply_markup=markup)

    


 
@bot.message_handler(content_types=['text'])
def info(message):
    if message.chat.type == 'private':
        ##информация
        if message.text == 'Информация':
            mes = 'Ресторан "Фигаро" вобрал в себя лучшие традиции европейской кухни'
            bot.send_message(message.chat.id, mes)
        #официант
        elif message.text == 'Подозвать официанта':
            ms = bot.send_message(message.chat.id, 'Укажите номер вашего столика:  ')
            bot.register_next_step_handler(ms, send_2)
        #забронировать место
        elif message.text == 'Бронь':
        	try:
        		chat_id = message.chat.id
        		user_dict[chat_id] = User(message.text)
        		markup = types.ReplyKeyboardRemove(selective=False)
        		msg = bot.send_message(chat_id, 'Укажите число и месяц, когда бы вы хотели забронировать стол ', reply_markup=markup)
        		bot.register_next_step_handler(msg, process_fullname_step)
        	except Exception as e:
        		msg = bot.reply_to(message, 'Вы ввели что то другое. Пожалуйста введите дату.')

     
        #отзыв
        elif message.text == 'Оставить отзыв':
            msg = bot.send_message(message.chat.id, 'Готов принять ваш отзыв:  ')
            bot.register_next_step_handler(msg, send_1)
        else:
        	mea = "Я вас не понимаю, выберите любую из предложенный команд"
        	bot.send_message(message.chat.id, mea)
    
        
  

            

    

def send_1(message):
    ok = bot.send_message(user_2, f'Сообщение от Пользователя ({message.chat.id}):\n{message.text}')
    bot.register_next_step_handler(ok, text)

def send_2(message):
    bot.send_message(message.chat.id, "Официант подойтек к вам через пару минут")
    bot.send_message(user_2, f'Клиент за столиком, под номером {message.text} ожидает официанта')

def send_3(message):
    bot.send_message(message.chat.id, "Спасибо, администратор свяжется с вами через пару минут")
    qq = bot.send_message(user_2, f'Клиент ({message.chat.id}) запросил бронь : {message.text}')
    bot.register_next_step_handler(qq, adm)

def adm(message):
    if message.reply_to_message:
        bot.send_message(''.join(re.findall(r'\d.*', message.reply_to_message.text.split('\n')[0])),
                         f'Сообщение от Администратора: \n{message.text}')
    else:
        msggg = bot.send_message(message.chat.id, 'возможен только ответ на сообщение')
        bot.register_next_step_handler(msggg, adm)




def text(message):
    if message.reply_to_message:
        bot.send_message(''.join(re.findall(r'\d.*', message.reply_to_message.text.split('\n')[0])),
                         f'Сообщение от Администратора: \n{message.text}')
    else:
        msg = bot.send_message(message.chat.id, 'возможен только ответ на сообщение')
        bot.register_next_step_handler(msg, text)


def process_fullname_step(message):
    try:

        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.fullname = message.text

        msg = bot.send_message(chat_id, 'Укажите точное время, на которое вы хотели забронировать стол')
        bot.register_next_step_handler(msg, process_phone_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')

def process_phone_step(message):
    try:
        

        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        msg = bot.send_message(chat_id, 'Укажите количество людей, с кем вы собираетесь посетить наш ресторан')
        bot.register_next_step_handler(msg, process_driverSeria_step)

    except Exception as e:
        msg = bot.reply_to(message, 'Вы ввели что то другое. Пожалуйста введите номер телефона.')
        bot.register_next_step_handler(msg, process_phone_step)

def process_driverSeria_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.driverSeria = message.text

        msg = bot.send_message(chat_id, 'Укажите ваш номер телефона для оперативной связи')
        bot.register_next_step_handler(msg, process_carDate_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_carDate_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.carDate = message.text

        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, getRegData(user, 'Вы указали', message.from_user.first_name), parse_mode="Markdown")
        # отправить в группу
        bot.send_message(user_2, getRegData(user, 'Бронь Бот:', bot.get_me().username), parse_mode="Markdown")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Оставить отзыв")
        item2 = types.KeyboardButton("Информация")
        item3 = types.KeyboardButton("Бронь")
        item4 = types.KeyboardButton("Подозвать официанта")
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.chat.id, "Хорошо, <b>{0.first_name}</b>,\nАдминистратор свяжется с вами через пару минут!".format(message.from_user, bot.get_me()),
        	parse_mode = 'html', reply_markup=markup)


    	

       



    except Exception as e:
        bot.send_message(message, "Спасибо")

# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"
def getRegData(user, title, name):


    t = Template('$title *$name* \n Дата: *$fullname* \n Время: *$phone* \n Люди: *$driverSeria* \n Телефон: *$carDate*')

    return t.substitute({
        'title': title,
        'name': name,
        'fullname': user.fullname,
        'phone': user.phone,
        'driverSeria': user.driverSeria,
        'carDate': user.carDate,
    })

#add items to markup



# произвольный текст


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()


bot.polling(none_stop=True)
