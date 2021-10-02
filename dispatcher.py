import logging
from aiogram import *
from filters import *
import config
from sqlite3 import *
from work_with_db import *

# Configure logging
logging.basicConfig(level=logging.INFO)

conn = connect("data_bases/tasks.db")
cur = conn.cursor()

# prerequisites
if not config.BOT_TOKEN:
    exit("No token provided")

# init
bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# activate filters
dp.filters_factory.bind(IsOwnerFilter)
dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(MemberCanRestrictFilter)

# дописать помощь + приветствие

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm Tester bot!\nMade by GoshiX.")

@dp.message_handler(commands=['random'])
async def send_welcome(message: types.Message):
    cond = random_condition()
    if (len(cond) == 1):
        await message.answer(cond[0])
    else:
        await message.answer(cond[0])
        await message.answer("Текст:")
        await message.answer(cond[1])

@dp.message_handler(commands=['id'])
async def send_welcome(message: types.Message):
    await message.reply(message.from_user.id)

@dp.message_handler(commands=['admin'])
async def send_welcome(message: types.Message):
    if (str(message.from_user.id) == str(config.BOT_OWNER)):
        await message.reply("You are owner!")
    else:
        await message.reply("Ops! You don't have permission to use this command((")

#tmp command

@dp.message_handler(commands=['double'])
async def send_welcome(message: types.Message):
    value = message.text
    await message.answer(value)

@dp.message_handler()
async def send_welcome(message: types.Message):
    if message.text[0] == "/":
        await message.answer("I don't know this command)\nYou can use /help")