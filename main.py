from aiogram import Bot, Dispatcher, types
import sys
import logging
import asyncio
import os
from aiogram import F
import json
from dotenv import load_dotenv, find_dotenv
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart, CommandObject, Command
from gpt import messaging, command_gpt
from openai import OpenAI
import gpt
import re
from aiogram.enums import ParseMode

load_dotenv(find_dotenv())
bot = Bot(os.getenv("TOKEN"), parse_mode='Markdown')
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(CommandStart())
async def start_command(message: types.Message):
    res = messaging("Привет")
    await message.answer(res)


@dp.message(F.text, Command("botGPT"))
async def command_sender(message: types.Message):
    res = command_gpt(message.text)

    await message.answer(res)


@dp.message()
async def Sender(message: types.Message):
    res = messaging(message.text)

    await message.answer(res)



@dp.message()
async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %('
                                                                      'message)s')
    asyncio.run(main())
