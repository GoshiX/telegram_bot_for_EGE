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
bot = Bot(token=config.BOT_TOKEN) #, parse_mode="HTML"
dp = Dispatcher(bot, storage=MemoryStorage())

# activate filters
dp.filters_factory.bind(IsOwnerFilter)
dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(MemberCanRestrictFilter)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    login(message.from_user.id)
    await message.reply("Добр пожаловать!\nЭтот бот создан для тренировки заданий из ЕГЭ по русскому языку.\n"
                        "Просите у бота вопрос, а затем введите ответ для его проверки\n"
                        "Создатель: @goshanmorev")

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("Список команд можно посмотреть рядом с полем ввода")

@dp.message_handler(commands=['random', 'r'])
async def send_welcome(message: types.Message):
    cond = random_condition(str(message.from_user.id))
    for i in cond:
        await message.answer(i)

@dp.message_handler(commands=['theme_list'])
async def send_welcome(message: types.Message):
    await message.answer("1. Информационная обработка текстов различных стилей и жанров\n"
                         "2. Средства связи предложений в тексте\n"
                         "3. Определение лексического значения слова\n"
                         "4. Постановка ударения\n"
                         "5. Употребление паронимов\n"
                         "6. Лексические нормы\n"
                         "7. Морфологические нормы (образование форм слова)\n"
                         "8. Синтаксические нормы. Нормы согласования. Нормы управления\n"
                         "9. Правописание корней\n"
                         "10. Правописание приставок\n"
                         "11. Правописание суффиксов (кроме -Н-/-НН-)\n"
                         "12. Правописание личных окончаний глаголов и суффиксов причастий\n"
                         "13. Правописание НЕ и НИ\n"
                         "14. Слитное, дефисное, раздельное написание слов\n"
                         "15. Правописание -Н- и -НН- в суффиксах\n"
                         "16. Пунктуация в сложносочиненном предложении и в предложении с однородными членами\n"
                         "17. Знаки препинания в предложениях с обособленными членами\n"
                         "18. Знаки препинания при словах и конструкциях, не связанных с членами предложения\n"
                         "19. Знаки препинания в сложноподчиненном предложении\n"
                         "20. Знаки препинания в сложных предложениях с разными видами связи\n"
                         "21. Постановка знаков препинания в различных случаях\n"
                         "22. Смысловая и композиционная целостность текста\n"
                         "23. Функционально-смысловые типы речи\n"
                         "24. Лексическое значение слова\n"
                         "25. Средства связи предложений в тексте\n"
                         "26. Языковые средства выразительности")

@dp.message_handler(commands=['statistics', 's'])
async def send_welcome(message: types.Message):
    await message.answer("Ждите следующую версию бота))")

@dp.message_handler(commands=['theme', 't'])
async def send_welcome(message: types.Message):
    msg = message.text
    theme_num = re.search('\d{1,}', msg)
    if (theme_num == None):
        await message.answer("Вам нужно ввести номер темы после запроса\n"
                             "Список тем: /theme_list")
        return
    theme_num = int(theme_num[0]) - 1
    if not (theme_num >= 0 and theme_num <= 25):
        await message.answer("Вы ввели некорректный номер темы.\n"
                             "Их всего 26.\n"
                             "Вот их список: /theme_list")
        return
    cond = theme_condition(theme_num, str(message.from_user.id))
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

@dp.callback_query_handler(text="random_value")
async def send_random_value(call: types.CallbackQuery):
    viv = get_explain(str(call.from_user.id))
    for i in viv:
        await call.message.answer(i)

@dp.message_handler()
async def not_coomand(message: types.Message):
    if message.text[0] == "/":
        await message.answer("Я не знаю такой команды\nИспользуйте /help")
    else:
        if str(if_ans(str(message.from_user.id))) == "1":
            correct = check_ans(str(message.from_user.id), message.text)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Нажмите для объяснения + ответа", callback_data="random_value"))
            if (correct == True):
                await message.answer("Молодец!\nВсё правильно", reply_markup=keyboard)
            else:
                await message.answer("Ты ошибся((", reply_markup=keyboard)