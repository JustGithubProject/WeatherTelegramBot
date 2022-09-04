import requests
import datetime
from config import token_tg_bot, open_weather_token
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=token_tg_bot)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Введите названия города: ")


@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&lang=ua&appid={open_weather_token}&units=metric")
        data = r.json()
        city = data['name']
        temp = data['main']['temp']
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        country = data['sys']['country']
        weather = data['weather'][0]['description']
        speed = data['wind']['speed']
        humidity = data['main']['humidity']
        await message.answer(
            f"Город: {city}\n Погода: {temp}°\n Восход солнца: {sunrise}\n Заход солнца: {sunset}\n Страна: {country}\n Внешне: {weather}\n Скорость ветра: {speed}м/c\n Влажность: {humidity}%")

    except Exception as ex:
        print(ex)
        print("Проверьте название города")





if __name__ == "__main__":
    executor.start_polling(dp)
