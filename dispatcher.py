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
    await message.reply("Добро пожаловать!\nЭтот бот создан для тренировки заданий из ЕГЭ по русскому языку.📝\n"
                        "Вы можете попросить бота выдать вам как случайный вопрос, так и вопрос по теме, после чего он проверит корректность введёного вами ответа.\n"
                        "Для корректной проверки ответы нужно писать слитно (даже без пробелов)\n"
                        "Помощь - /help\n"
                        "Создатель: @goshanmorev")

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("Список команд:\n\n"
                        "/random - Случайный вопрос 🎲\n"
                        "/r - Случайный вопрос 🎲\n\n"
                        "/theme - Вопрос по теме❔\n"
                        "/t - Вопрос по теме❔\n\n"
                        "/statistics - Ваша статистика📈\n"
                        "/s - Ваша статистика📈\n\n"
                        "/theme_list - Список тем📋\n"
                        "/id - Ваш id")

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
    await message.answer(ret_stat(str(message.from_user.id)))

@dp.message_handler(commands=['user_info'])
async def send_welcome(message: types.Message):
    msg = message.text
    user_id = re.search('\d{1,}', msg)
    if (str(message.from_user.id) == str(config.BOT_OWNER) or check_admin(str(message.from_user.id))):
        if (user_id != None):
            await message.answer(ret_stat(str(int(user_id[0]))))
    else:
        await message.reply("Ops! You don't have permission to use this command((")

@dp.message_handler(commands=['theme', 't'])
async def send_welcome(message: types.Message):
    msg = message.text
    theme_num = re.search('\d{1,}', msg)
    if (theme_num == None):
        await message.answer("Введите номер темы.")
        wait_theme(str(message.from_user.id))
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
    msg = message.text
    admin_id = re.search('\d{1,}', msg)
    if (str(message.from_user.id) == str(config.BOT_OWNER) or check_admin(str(message.from_user.id))):
        await message.reply("You are owner!")
        if (admin_id != None):
            give_admin(str(int(admin_id[0])))
            await message.reply("Ок")
    else:
        await message.reply("Ops! You don't have permission to use this command((")

@dp.callback_query_handler(text="random_value")
async def send_random_value(call: types.CallbackQuery):
    viv = get_explain(str(call.from_user.id))
    for i in viv:
        await call.message.answer(i)

@dp.callback_query_handler(text="question_value")
async def send_new_quest(call: types.CallbackQuery):
    q = rand_more(str(call.from_user.id))
    if (q[0] == True):
        cond = random_condition(str(call.from_user.id))
        for i in cond:
            await call.message.answer(i)
    else:
        cond = theme_condition(q[1], str(call.from_user.id))
        for i in cond:
            await call.message.answer(i)

@dp.message_handler()
async def not_coomand(message: types.Message):
    if message.text[0] == "/":
        await message.answer("Я не знаю такой команды\nИспользуйте /help")
    elif if_theme(str(message.from_user.id)) == True:
        msg = message.text
        theme = re.search('\d{1,}', msg)
        if theme == None:
            await message.answer("Введите номер темы\n"
                                 "Вот их список: /theme_list")
            return
        theme = int(theme[0])
        theme -= 1
        if not (theme >= 0 and theme <= 25):
            await message.answer("Вы ввели некорректный номер темы.\n"
                                 "Их всего 26.\n"
                                 "Вот их список: /theme_list")
            return
        not_wait_theme(str(message.from_user.id))
        cond = theme_condition(theme, str(message.from_user.id))
        for i in cond:
            await message.answer(i)
    elif str(if_ans(str(message.from_user.id))) == "1":
            correct = check_ans(str(message.from_user.id), message.text)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Нажмите для объяснения + ответа", callback_data="random_value"))
            keyboard.add(types.InlineKeyboardButton(text="Ещё вопрос", callback_data="question_value"))
            add_stat(str(message.from_user.id), correct)
            if (correct == True):
                await message.answer("Молодец!\nВсё правильно✔", reply_markup = keyboard)
            else:
                await message.answer("Ты ошибся((✖", reply_markup=keyboard)