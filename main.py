from aiogram import Bot, Dispatcher, F
import asyncio
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
import requests
import json
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = Bot(token='6463042527:AAG8fXrkCRwVmIcIEolZVTJAw4ojqD81JU8')
dp = Dispatcher()

apikey = 'f6ea85f695a369d64aafe02f4ac98d92'


@dp.message(CommandStart())
async def start(message: Message):
    btn1 = KeyboardButton(text='Получить прогноз погоды')
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]], resize_keyboard=True)
    await message.answer(f'Привет, {message.from_user.first_name}, чем я могу Вам помочь?',
                         reply_markup=markup)


@dp.message(F.text == 'Получить прогноз погоды')
async def weather(message: Message):
    await message.answer('Введите город')


@dp.message(F.text)
async def city(message: Message):
    city = message.text.lower().strip()
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&appid={apikey}&units=metric'
    res = requests.get(url)
    data = json.loads(res.text)
    if res.status_code == 200:
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = int(data['main']['pressure'])
        pressure = round(pressure / 133.3 * 100, 1)
        wind_speed = data['wind']['speed']
        desc = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        photo = f'img/{icon}@2x.png'
        emoji = ['🌡', '💧', '💥', '💨']
        await message.answer_photo(photo=FSInputFile(photo),
                                   caption=f'Погода в городе {message.text}:\n'
                                           f'Температура: {temp}°C{emoji[0]}\n'
                                           f'Влажность воздуха: {humidity}%{emoji[1]}\n'
                                           f'Атмосферное давление: {pressure} мм рт.ст{emoji[2]}\n'
                                           f'Скорость ветра: {wind_speed} м/с{emoji[3]}\n'
                                           f'Описание: {desc}\n')
    elif res.status_code == 404:
        await message.answer('Город не найден')


dp.message.register(city, F.text)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
