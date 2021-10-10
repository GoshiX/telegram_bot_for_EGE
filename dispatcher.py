import logging
import re
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
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
dp = Dispatcher(bot, storage=MemoryStorage())

# activate filters
dp.filters_factory.bind(IsOwnerFilter)
dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(MemberCanRestrictFilter)

class Mydialog(StatesGroup):
    waiting_ans = State()
    ans = []

class explanation(StatesGroup):
    exp_out = ""

# дописать помощь + приветствие

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    login(message.from_user.id)
    await message.reply("Hi!\nI'm Tester bot!\nMade by GoshiX.")

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm Tester bot!\nMade by GoshiX.")

@dp.message_handler(commands=['random'])
async def send_welcome(message: types.Message):
    cond, answer, explanation.exp_out = random_condition()
    for i in cond:
        await message.answer(i)
    await Mydialog.waiting_ans.set()
    Mydialog.ans = answer

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
    cond, answer, explanation.exp_out = theme_condition(theme_num)
    for i in cond:
        await message.answer(i)
    await Mydialog.waiting_ans.set()
    Mydialog.ans = answer

@dp.message_handler(commands=['id'])
async def send_welcome(message: types.Message):
    await message.reply(message.from_user.id)

@dp.message_handler(commands=['admin'])
async def send_welcome(message: types.Message):
    if (str(message.from_user.id) == str(config.BOT_OWNER)):
        await message.reply("You are owner!")
    else:
        await message.reply("Ops! You don't have permission to use this command((")

@dp.message_handler(state = Mydialog.waiting_ans)
async def process_message(message: types.Message, state: FSMContext):
    await state.finish()
    right = False
    for i in Mydialog.ans:
        if (message.text == i):
            right = True
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="random_value"))
    if (right):
        await message.answer("Молодец!\nВсё правильно", reply_markup=keyboard)
    else:
        await message.answer("Ты ошибся((", reply_markup=keyboard)

@dp.callback_query_handler(text="random_value")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer(explanation.exp_out)

@dp.message_handler()
async def not_coomand(message: types.Message):
    if message.text[0] == "/":
        await message.answer("I don't know this command)\nYou can use /help")