TOKEN='1880772212:AAFb7ULr5P0ps_MnHDL3IAcxG6Uooeejkyc'
from random import randint,choice
from requests import get
from bs4 import BeautifulSoup
import  telebot
from telebot import types

def get_random_compliment():
    random_page_number=str(randint(1,97))
    webpage=get('http://kompli.me/komplimenty/page/'+random_page_number).text
    tags=BeautifulSoup(webpage,'html.parser').find_all('a')
    compliments=[]
    for tag in tags:
        tag_text=tag.get_text()
        if tag_text=='Назад':
            break
        compliments.append(tag_text)
    return choice(compliments[4:])

def get_dollars():
    webpage=get('https://www.banki.ru/products/currency/cash/eur/moskva/').text
    tags = BeautifulSoup(webpage, 'html.parser').find('tbody')
    spisok=[]
    tag=tags.find('div',class_='currency-table__large-text')
    spisok.append(tag.get_text())
    return spisok[0]

def get_euro():
    webpage=get('https://www.banki.ru/products/currency/cash/eur/moskva/').text
    tags = BeautifulSoup(webpage, 'html.parser').find('tbody')
    spisok=[]
    tag=tags.find('div',class_='currency-table__large-text')
    spisok.append(tag.get_text())
    return spisok[0]
bot = telebot.TeleBot(TOKEN);

user_num1 = ''
user_num2 = ''
user_proc = ''
user_result = None
def process_num1_step(message, user_result = None):
    try:
       global user_num1
       if user_result == None:
          user_num1 = int(message.text)
       else:
          user_num1 = str(user_result)
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
       itembtn1 = types.KeyboardButton('+')
       itembtn2 = types.KeyboardButton('-')
       itembtn3 = types.KeyboardButton('*')
       itembtn4 = types.KeyboardButton('/')
       markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

       msg = bot.send_message(message.chat.id, "Выберите операцию", reply_markup=markup)
       bot.register_next_step_handler(msg, process_proc_step)
    except Exception as e:
       bot.reply_to(message, 'Это не число или что то пошло не так...')
def process_proc_step(message):
    try:
       global user_proc
       user_proc = message.text
       markup = types.ReplyKeyboardRemove(selective=False)
       msg = bot.send_message(message.chat.id, "Введите еще число", reply_markup=markup)
       bot.register_next_step_handler(msg, process_num2_step)
    except Exception as e:
       bot.reply_to(message, 'Вы ввели что то другое или что то пошло не так...')
def process_num2_step(message):
    try:
       global user_num2
       user_num2 = int(message.text)
       markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
       itembtn1 = types.KeyboardButton('Результат')
       itembtn2 = types.KeyboardButton('Продолжить вычисление')
       markup.add(itembtn1, itembtn2)
       msg = bot.send_message(message.chat.id, "Показать результат или продолжить операцию?", reply_markup=markup)
       bot.register_next_step_handler(msg, process_alternative_step)
    except Exception as e:
       bot.reply_to(message, 'Это не число или что то пошло не так...')
def process_alternative_step(message):
    try:
       calc()
       user_markup=telebot.types.ReplyKeyboardMarkup(True,False)
       user_markup.row('Комплимент','Калькулятор')
       user_markup.row('Курс доллара','Курс евро')
       if message.text.lower() == 'результат':
          bot.send_message(message.chat.id, calcResultPrint(), reply_markup=user_markup)
       elif message.text.lower() == 'продолжить вычисление':
          process_num1_step(message, user_result)

    except Exception as e:
       bot.reply_to(message, 'Что то пошло не так...')
def calc():
    global user_num1, user_num2, user_proc, user_result
    user_result = eval(str(user_num1) + user_proc + str(user_num2))
    return user_result
def calcResultPrint():
    global user_num1, user_num2, user_proc, user_result

    return "Результат: " + str(user_num1) + ' ' + user_proc + ' ' + str(user_num2) + ' = ' + str( user_result )

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup=telebot.types.ReplyKeyboardMarkup(True,False)
    user_markup.row('Комплимент','Калькулятор')
    user_markup.row('Курс доллара','Курс евро')
    bot.send_message(message.from_user.id,'Добро пожаловать!',reply_markup=user_markup)

@bot.message_handler(commands=['stop'])
def handle_start(message):
    hide_markup=telebot.types.ReplyKeyboardHide()
    bot.send_message(message.from_user.id,'..',reply_markup=hide_markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/comp" or message.text == "Комплимент":
        bot.send_message(message.from_user.id, "Привет, держи комплимент")
        bot.send_message(message.from_user.id, get_random_compliment())
    elif message.text=="/dollar" or message.text == "Курс доллара":
        bot.send_message(message.from_user.id, "Курс доллара к рублю:")
        bot.send_message(message.from_user.id, get_dollars())
    elif message.text=="/euro"or message.text == "Курс евро":
        bot.send_message(message.from_user.id, "Курс евро к рублю:")
        bot.send_message(message.from_user.id, get_euro())
    elif message.text=="/calc"or message.text == "Калькулятор":
        bot.send_message(message.from_user.id, 'Введите первое число:')
        bot.register_next_step_handler(message, process_num1_step)
    elif message.text=='/help':
        bot.send_message(message.from_user.id, "Я специально созданный бот студента 2 курса, я могу вам показать курс евро к рублю,если вы введете 'Курс евро' или /euro \
        также я  могу вам показать курс доллара к рублю,если вы введете 'Курс доллара' или /dollar, а так же во мне заложены такие функции как калькулятор (Калькулятор;/calc) \
        или прислать комплимент (Комплимент;/comp)")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
bot.polling(none_stop=True, interval=0)
