import telebot
from telebot import types
import requests
import json
import datetime #---Для преобразования UNIX кода времени в удобочитаемый формат.
#---Токен бота: "5399221206:AAFu23E3eszo8cTKmxxa1stLvsDLkyRUn14"
#---apiToken = "a131f75fed65d9b30b5cef60ad696592"

bot = telebot.TeleBot("5399221206:AAFu23E3eszo8cTKmxxa1stLvsDLkyRUn14")
apiToken = "a131f75fed65d9b30b5cef60ad696592"

#---СПИСОК ПЕРЕМЕННЫХ.
outsideTemperature = 0                      #---Температура воздуха.
pressure = 0                                #---Давление воздуха.
humidity = 0                                #---Влажность воздуха.
windSpeed = 0                               #---Скорость ветра.
c = u'\u2103'                               #---Знак градуса цельсия.


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Введите название города, в котором хотите узнать погоду:")


@bot.message_handler()
def weather(message):
    try:
        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorn": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
        }


        sity = message.text
        params = {"q": sity, "appid": apiToken,
                  "units": "metric"}  # ---Ключ запроса q и текст запроса.   Здесь формируем запрос.
        addres = requests.get('https://api.openweathermap.org/data/2.5/weather',
                              params=params)  # ---Отправляем запрос сайту.
        formatGet = addres.json()  # ---Помещаем в переменную "y" полученную информацию преобразовав ее в json формат.

        weatherDescription = formatGet["weather"][0]["main"]  #---для подключения смайлов.
        if weatherDescription in code_to_smile:
            addSmile = code_to_smile[weatherDescription]
        else:
            bot.send_message(message.chat.id, "smailnow.")


        outsideTemperature = formatGet["main"]["temp"]   # ---Температура воздуха.
        pressure = formatGet["main"]["pressure"]         # ---Давление воздуха.
        humidity = formatGet["main"]["humidity"]         # ---Влажность воздуха.
        windSpeed = formatGet["wind"]["speed"]           # ---Скорость ветра.
        sityName = formatGet["name"]                     #---Название города.
        sunrise_time = datetime.datetime.fromtimestamp(formatGet["sys"]["sunrise"])        #---Восход солнца.
        sunset_time = datetime.datetime.fromtimestamp(formatGet["sys"]["sunset"])          #---Закат солнца.
        # --------------------------------------------------------------------БЛОК ВЫВОДА ИНФОРМАЦИИ
        bot.send_message(message.chat.id, f"<b>\U0001F30F Погода в городе {sityName}:</b>", parse_mode="html")
        bot.send_message(message.chat.id, f" Температура воздуха: {outsideTemperature}{c} {addSmile}\n"
                                          f" Скорость ветра: {windSpeed} м/с\n"
                                          f" Давление воздуха: {pressure} мм.рт.ст\n"
                                          f" Влажность воздуха: {humidity} мбар.\n"
                                          f" Восход солнца: {sunrise_time} \n"
                                          f" Закат солнца: {sunset_time}")
    except:
        bot.send_message(message.chat.id, "Проверьте название города \U00002639")



bot.infinity_polling()
