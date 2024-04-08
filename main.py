from aiogram import Bot, Dispatcher, types
import sys
import logging
import asyncio
import os
from aiogram import F
import json
from dotenv import load_dotenv, find_dotenv
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart,  Command
from gpt import messaging, command_gpt

"""Конфиги """
load_dotenv(find_dotenv())
bot = Bot(os.getenv("TOKEN"), parse_mode='Markdown')
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


"""Стартовое сообщение """
@dp.message(CommandStart())
async def start_command(message: types.Message):
    res = messaging("Привет")
    bissness = message.business_connection_id
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text=res, business_connection_id=bissness)

"""Отправка бизнес сообщений """
@dp.business_message(F.text)
async def business_mess(message: types.Message):
    if message.from_user.id != os.getenv("ID"):
        res = messaging(message.text)
        business = message.business_connection_id
        chat_id = message.chat.id
        await bot.send_message(chat_id=chat_id, text=res, business_connection_id=business)


"""Отправка обычных сообщений (структурирование сообщений) """
@dp.message(F.text, Command("gpt"))
async def command_sender(message: types.Message):
    res = command_gpt(message.text)

    await message.answer(res)

"""Отправка обычных сообщений (не для бизнес аккаунта) """
@dp.message()
async def Sender(message: types.Message):
    res = messaging(message.text)

    business = message.business_connection_id
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text=res, business_connection_id=business)


"""Запуск бота """
@dp.message()
async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %('
                                                                      'message)s')
    asyncio.run(main())
