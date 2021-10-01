import logging
from aiogram import *
from filters import IsOwnerFilter, IsAdminFilter, MemberCanRestrictFilter
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

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm Tester bot!\nMade by GoshiX.")

@dp.message_handler(commands=['q'])
async def send_welcome(message: types.Message):
    await message.answer(random_condition())