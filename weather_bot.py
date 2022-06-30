from aiogram import Bot, Dispatcher, executor, types
import conf,logging

from conf import token_weather #Берём токен с ресурса OpenWeather(именно он выдаёт погоду)
import requests #Для парсинга данных
"""############### ФУНКЦИЯ ДЛЯ ОПРЕДЕЛЕНИЯ ПОГОДЫ ##################"""
def weather_func(city,token_weather): #город и токен
    try:
        #Парсим данные по городу установив русский язык и выбрав Цельсия
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&appid={token_weather}&units=metric")
        page = r.json()
        #Разбираем из страницы нужные нам данные
        name_of_city = f'🏛 Город: {page["name"]}\n\n' #Название города
        some_information = f' {page["weather"][0]["description"]}\n\n' #Кратко о погоде
        wind_speed = f'🍃 Ветер: {page["wind"]["speed"]} м/с\n' #Скорость ветра
        visibility = f'👀 Видимость: {page["visibility"]} м\n' #Видимость
        feels_like = f'💭 Ощущается как: {page["main"]["feels_like"]}°C\n' #Ощущается как
        humidity = f'💦 Влажность: {page["main"]["humidity"]}%\n' #Влажность
        pressure = f'⭕ Давление: {page["main"]["pressure"]} мм.рт.ст\n' #Давление
        temperature = f'🌡 {page["main"]["temp"]}°C\n\n' #Темература
        interval_temp = f'♾ Колебания от {page["main"]["temp_min"]}°C до {page["main"]["temp_max"]}°C\n'
        big_text = f"{name_of_city}{some_information.capitalize()}{temperature}{feels_like}{interval_temp}{wind_speed}{visibility}{humidity}{pressure}"
        return big_text
    except Exception as e:
        return "Проверь название города!"


#Объект бота
bot = Bot(token=conf.config['token'])

#Диспетчер бота для команд
dp = Dispatcher(bot)

#Включаем логи чтобы ничего не упустить
logging.basicConfig(level=logging.INFO)

"""############### БЛОК КОМАНД БОТА ##################"""
#Реакция на команду /start
@dp.message_handler(commands=["start"])
async def startt(message: types.Message): #Используем message для краткой записи types.Message
    #Внизу приветствующее сообщение бота + функция для удаления команд пользователя после их ввода
    messag = f'Привет <u>{message.from_user.full_name}</u>,меня зовут <b>☀ WEATHER_WORLD BOT ☀</b>\n✅ Скорее пиши /help и узнай все мои возможности!'
    await bot.send_message(message.chat.id, messag, parse_mode='html')
    await message.delete()

# Реакция на команду /help
@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    # Создали разметку на 2 кнопки в каждом ряду + подрегулировали размер
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    weatherr = types.KeyboardButton('🌤 Узнать погоду')  # Кнопка №1
    stop = types.KeyboardButton('🛑 Stop')  # Кнопка №2
    markup.add(weatherr,stop) # Закидываем в разметку
    #Отсылаем их
    await bot.send_message(message.chat.id, 'У меня функция всего одна,нажми скорей и будет твоя!', reply_markup=markup)
    await message.delete() # Функция для удаления команд пользователя после их ввода

#Реакция на команду /stop
@dp.message_handler(commands=["stop"])
async def stopp(message: types.Message):
    await dp.stop_polling()
    await message.delete()


"""############### КЛИЕНТСКАЯ ЧАСТЬ ##################"""
@dp.message_handler(content_types=["text"])
async def textt(message: types.Message):
    if 'погод' in message.text.lower(): # Если прозвучало слово погода/сработала кнопка то даём инструкции
        await bot.send_message(message.chat.id, f'<b>🏛 Введи свой город 🌤</b>', parse_mode='html')
    elif message.text.lower() == '🛑 stop':  # На stop вызываем функцию остановки,либо пропишем /stop и она так же сработает напрямую
        await stopp(message.text)
    else: # После ввода города,запускаем нашу фукция с OpenWeather
        await bot.send_message(message.chat.id,f'<b>{weather_func(message.text,token_weather)}</b>',parse_mode='html')

#Запускаем цикл работы бота с skip updates,для того чтобы когда бот не онлайн ему не слали смс
executor.start_polling(dp,skip_updates=True)

























