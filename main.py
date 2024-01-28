from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

app.run(host='0.0.0.0', port=81)

import g4f
from pymongo.mongo_client import MongoClient
import time

uri = "mongodb+srv://Cola:ungeziefer@cluster0.6qvvna5.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
#collection = client[HalykLife]

classes = ["Калькулятор цены и ценообразования страховки", "Оформление страховки", "Вопрос по поводу страхования", "Прочее", "Отмена операции"]

js_tarfs = {
    "Покрываемые риски" : {
        "Минимально базовый тариф" : {
            "Смерть" : 0.0835,
            "Установление инвалидности I группы" : 0.0029,
            "Установление инвалидности II группы" : 0.0132,
            "Установление инвалидности III группы" : 0.0015,
            "Получение телесной травмы" : 0.0073,
            "Установление временной нетрудоспособности" : 0.0308,
            "Госпитализация" : 0.0073
        },
        "Базовый тариф" : {
            "Смерть" : 0.1737,
            "Установление инвалидности I группы" : 0.0061,
            "Установление инвалидности II группы" : 0.0274,
            "Установление инвалидности III группы" : 0.0030,
            "Получение телесной травмы" : 0.0152,
            "Установление временной нетрудоспособности" : 0.0640,
            "Госпитализация" : 0.0152
        },
        "Mаксимально базовый тариф" : {
            "Смерть" : 0.9044,
            "Установление инвалидности I группы" : 0.0317,
            "Установление инвалидности II группы" : 0.1428,
            "Установление инвалидности III группы" : 0.0159,
            "Получение телесной травмы" : 0.0793,
            "Установление временной нетрудоспособности" : 0.3332,
            "Госпитализация" : 0.0793
        }
    }
}

js_factors = {
    "Минимальный риск" : {
        "Профессия" : 0.20,
        "Наличие страховых случаев" : 0.25,
        "Возраст застрахованного" : 0.25,
        "Занятия активным отдыхом" : 0.25
    },
    "Средний риск" : {
        "Профессия" : 1.85,
        "Наличие страховых случаев" : 1.65,
        "Возраст застрахованного" : 1.50,
        "Занятия активным отдыхом" : 1.45
    },
    "Максимальный риск" : {
        "Профессия" : 3.5,
        "Наличие страховых случаев" : 3,
        "Возраст застрахованного" : 2.8,
        "Занятия активным отдыхом" : 2.5
    }
}

def op_calculator():
    user_tarfs = input("Введите ваши тарифы (Справка по тарифам: https://www.halyklife.kz/storage/app/media/%20%D1%82%D0%B0%D1%80%D0%B8%D1%84%D1%8B_rus.pdf): ")
    time.sleep(0.5)
    tarifs = g4f.ChatCompletion.create(
        model=g4f.models.default,
        messages=[{"role": "user",
        "content": f"Возьми тарифы пользователя {user_tarfs} и возьми числовые значения из этого json {js_tarfs}, ничего не говори, просто дай список числовых значений, ничего больше"}],
        proxy="http://host:8080",
        timeout=120,
    )
    user_koefs = input("Введите ваш возраст, сколько у вас было страховых случаев и ваша профессия: ")
    koefs = g4f.ChatCompletion.create(
        model=g4f.models.default,
        messages=[{"role": "user",
        "content": f"Возьми ответы пользователя {user_koefs} и возьми числовые значения из этого json {js_factors}, ничего не говори, просто дай список числовых значений, ничего больше"}],
        proxy="http://host:8080",
        timeout=120,
    )
    halanswer = g4f.ChatCompletion.create(
        model=g4f.models.default,
        messages=[{"role": "user",
        "content": f"Бери тарифы пользователя {tarifs} и его коэффициенты риска {koefs} и скажи сколько будет стоить страховка если человек возьмет ее на 10 000 тенге"}],
        proxy="http://host:8080",
        timeout=120,
    )
    print(halanswer)

welcome_message = g4f.ChatCompletion.create(
    model=g4f.models.default,
    messages=[{"role": "user", "content": "Представь что ты банковский консультант банка HalykBank. Начни с приветствия 'Здравствуйте! Я ваш Halyk ассистент'"}],
    proxy="http://host:8080",
    timeout=120,
)
print(welcome_message)

answer = input(": ")
def responce(message):
    time.sleep(0.5)
    what = g4f.ChatCompletion.create(
        model=g4f.models.default,
        messages=[{"role": "user",
        "content": f"Тебе даны классы запросов клиентов: {classes}. Определи к какому классу подходит данный запрос пользователя: {message}. В ответе укажи только название класса и больше ничего, даже дополнительных символов не нужно"}],
        proxy="http://host:8080",
        timeout=120,
    )
    operation(what)

def operation(what):
    if what == classes[0]:
        
        op_calculator()

responce(answer)
