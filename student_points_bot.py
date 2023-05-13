import telebot
import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')

bot = telebot.TeleBot(token)

API_ENDPOINT = 'http://127.0.0.1:8000/api/v1/'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "👋 Привет! Напиши свою Фамилию и Имя")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    url = API_ENDPOINT + 'students/'
    params = {'format': 'json', 'search': message.text}
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        json = resp.json()
        #print(json)
        for key in json:
            bot.send_message(message.from_user.id, print_student_info(key))
    else:
        bot.send_message(message.from_user.id, "Не найдено :(")


def print_student_info(student):
    text = ""
    points = 0
    text += "Имя: " + student["student_name"] + "\n"
    for key in student["points"]:
        text += "- " + key["event"] + ": " + str(key["point"]) + "\n"
        points += key["point"]
    text += "Всего баллов: " + str(points)
    return text

bot.polling(none_stop=True, interval=0)
