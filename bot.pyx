import asyncio
import random
from aiogram import Bot, Dispatcher, types

# === НАСТРОЙКИ ===
TOKEN = "8662927935:AAGVLDcdCJPNM_ujdYeMeVRWd7pHdS6fP-k"  # Замени на токен от BotFather
CHANCE = 0.20                 # 20% шанс (0.20 = 20%)

# === БОТ ===
bot = Bot(token=TOKEN)
dp = Dispatcher()

# === ГЛАВНЫЙ ОБРАБОТЧИК ===
@dp.message()
async def on_message(message: types.Message):
    # Пропускаем команды (сообщения начинающиеся с /)
    if message.text and message.text.startswith('/'):
        return
    
    # Пропускаем сообщения от самого бота
    try:
        me = await bot.me()
        if message.from_user.id == me.id:
            return
    except:
        pass
    
    # Проверяем шанс 20%
    if random.random() < CHANCE:
        # Отправляем сообщение "вы получили очко"
        await message.answer("вы получили очко")

# === ЗАПУСК ===
async def main():
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())

