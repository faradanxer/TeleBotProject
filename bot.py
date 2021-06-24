TOKEN='1880772212:AAFb7ULr5P0ps_MnHDL3IAcxG6Uooeejkyc'
from random import randint,choice
from requests import get
from bs4 import BeautifulSoup
import telebot;
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
print(get_random_compliment())

bot = telebot.TeleBot(TOKEN);
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
bot.polling(none_stop=True, interval=0)