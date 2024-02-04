from aiogram import Bot, Dispatcher, types
import sys
import logging
import asyncio
import os
import json
from dotenv import load_dotenv, find_dotenv
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart, CommandObject, Command
from gpt import Messaging
from openai import OpenAI
import gpt
load_dotenv(find_dotenv())
bot = Bot(os.getenv("TOKEN"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(CommandStart())
async def start_command(message: types.Message):
    res = Messaging("Привет")
    await message.answer(res)


@dp.message()
async def Sender(message: types.Message):
    res = Messaging(message.text)

    await message.answer(res)

@dp.message()
async def main() -> None:
    await dp.start_polling(bot)




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %('
                                                                      'message)s')
    asyncio.run(main())