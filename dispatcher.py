import logging
import re
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
    for i in cond:
        await message.answer(i)

@dp.message_handler(commands=['theme'])
async def send_welcome(message: types.Message):
    msg = message.text
    theme_num = re.search('\d{1,}', msg)
    if (theme_num == None):
        await message.answer("Try again!")
        return
    theme_num = int(theme_num[0]) - 1
    if not (theme_num >= 0 and theme_num <= 25):
        await message.answer("Try again!")
        return
    cond = theme_condition(theme_num)
    for i in cond:
        await message.answer(i)

@dp.message_handler(commands=['id'])
async def send_welcome(message: types.Message):
    await message.reply(message.from_user.id)

@dp.message_handler(commands=['admin'])
async def send_welcome(message: types.Message):
    if (str(message.from_user.id) == str(config.BOT_OWNER)):
        await message.reply("You are owner!")
    else:
        await message.reply("Ops! You don't have permission to use this command((")

@dp.message_handler()
async def send_welcome(message: types.Message):
    if message.text[0] == "/":
        await message.answer("I don't know this command)\nYou can use /help")

#tmp command

"""
@dp.message_handler(commands=['double'])
async def send_welcome(message: types.Message):
    value = message.text[8:]
    res = re.search('\d{1,}', value)
    if (res == None):
        await message.answer("Try again!")
    else:
        await message.answer(int(res[0]) * 2)
"""