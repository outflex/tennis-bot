import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random
import os
import asyncio

# Получаем API токен из переменной окружения
API_TOKEN = os.getenv('API_TOKEN')

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=API_TOKEN)

# Инициализация диспетчера
dp = Dispatcher()

# Клавиатура для бота
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton('Начать обучение'))

next_step_menu = ReplyKeyboardMarkup(resize_keyboard=True)
next_step_menu.add(KeyboardButton('Следующий шаг'), KeyboardButton('Главное меню'))

retry_menu = ReplyKeyboardMarkup(resize_keyboard=True)
retry_menu.add(KeyboardButton('Начать обучение'))

# Список шагов обучения с изображениями
steps = [
    {
        "text": "Привет! Давайте начнем с основ большого тенниса.\n\nТеннис - это игра между двумя игроками (одиночные игры) или двумя командами по два игрока (парные игры), где игроки по очереди отбивают мяч через сетку с помощью ракетки.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/2/2b/Tennis_ball_and_racket.jpg"
    },
    {
        "text": "Основные правила:\n1. Матч состоит из нескольких сетов. Каждый сет состоит из геймов.\n2. Игроки начинают с подачи, и если мяч попадает в корт соперника, это очко.\n3. Игроки по очереди подают, а соперник должен попытаться отбить мяч, чтобы заработать очко.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/9/9e/Tennis_rules.png"
    },
    {
        "text": "Как считаются очки:\n1. Счет в гейме идет как 15, 30, 40, и затем выигрывается гейм, если игрок выигрывает два очка подряд после 40-40 (действие называется «деус»).\n2. После выигрыша гейма игрок получает один выигранный сет, который состоит из 6 геймов (если ничья, то играют тайбрейк).",
        "image": "https://upload.wikimedia.org/wikipedia/commons/e/e3/Tennis_score_example.jpg"
    },
    {
        "text": "Как считается сет:\n1. Сет состоит из 6 геймов, но если счет 5-5, то необходимо выиграть с разницей в два гейма (например, 7-5).\n2. Если счет 6-6, играют тайбрейк, где первый игрок, набравший 7 очков с разницей в два, выигрывает сет.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Tennis_foul.png"
    },
    {
        "text": "Фолы и ошибки:\n1. Подавать можно только дважды, если оба удара не попали в корт, то это фол и очко переходит к сопернику.\n2. Если мяч выходит за пределы корта или касается сетки, это ошибка.\n3. Нельзя касаться сетки ракеткой или телом во время розыгрыша.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/e/e1/Tennis_error.png"
    },
    {
        "text": "Виды ударов: 1. Форхенд (удар с передней стороны). 2. Бэкхенд (удар с задней стороны). 3. Слайс (удар с низким мячом). 4. Лоб (удар, поднимающий мяч высоко над соперником).",
        "image": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Tennis_shottypes.png"
    },
    {
        "text": "Типы покрытия: 1. Травяное покрытие (ускоряет мяч). 2. Грунтовое покрытие (замедляет мяч). 3. Хард (средняя скорость).",
        "image": "https://upload.wikimedia.org/wikipedia/commons/9/9a/Tennis_court_3_surface_types.png"
    },
    {
        "text": "Поздравляю! Вы завершили обучение. Теперь давайте проверим ваши знания.",
        "image": None
    }
]

# Вопросы для викторины
quiz_questions = [
    {"question": "Какой счет идет в теннисе после 30-30?", "options": ["40-30", "15-30", "40-40"], "answer": "40-30"},
    {"question": "Что происходит, если мяч касается сетки на подаче?", "options": ["Это фол", "Это нормально", "Подавать снова"], "answer": "Это фол"},
    {"question": "Как называется момент, когда счет 40-40?", "options": ["Деус", "Гейм", "Сет"], "answer": "Деус"},
    {"question": "Сколько геймов должно быть в сете для победы?", "options": ["5", "6", "7"], "answer": "6"},
    {"question": "Что такое тайбрейк?", "options": ["Это способ игры при 6-6", "Это ошибка", "Это спецудар"], "answer": "Это способ игры при 6-6"}
]

# Сложность викторины зависит от ответов пользователя
user_progress = {}

# Обработчик команд
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я помогу тебе разобраться в правилах большого тенниса. Для начала нажми 'Начать обучение'.", reply_markup=main_menu)

# Обработчик кнопки "Начать обучение"
@dp.message_handler(lambda message: message.text == 'Начать обучение')
async def start_training(message: types.Message):
    await message.reply(steps[0]["text"], reply_markup=next_step_menu)
    await bot.send_photo(message.chat.id, steps[0]["image"])
    global current_step
    current_step = 1  # Начинаем с первого шага

# Обработчик следующих шагов
@dp.message_handler(lambda message: message.text == 'Следующий шаг')
async def next_step(message: types.Message):
    global current_step
    if current_step < len(steps) - 1:  # Не превышаем пределы
        await message.reply(steps[current_step]["text"], reply_markup=next_step_menu)
        if steps[current_step]["image"]:
            await bot.send_photo(message.chat.id, steps[current_step]["image"])
        current_step += 1
    else:
        await message.reply(steps[current_step]["text"], reply_markup=types.ReplyKeyboardRemove())
        if steps[current_step]["image"]:
            await bot.send_photo(message.chat.id, steps[current_step]["image"])
        await message.answer("Теперь давайте проверим ваши знания!", reply_markup=retry_menu)
        await quiz(message)

# Викторина
async def quiz(message: types.Message):
    question = random.choice(quiz_questions)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for option in question["options"]:
        markup.add(KeyboardButton(option))

    await message.answer(question["question"], reply_markup=markup)

    # Ожидание ответа
    @dp.message_handler(lambda message: message.text in question["options"])
    async def check_answer(message: types.Message):
        if message.text.lower() == question["answer"].lower():
            user_progress[message.from_user.id] = user_progress.get(message.from_user.id, 0) + 1
            await message.answer("Правильно! Поздравляю! Вы прошли обучение.")
        else:
            await message.answer(f"Неправильно. Правильный ответ: {question['answer']}")
        await message.answer("Если хотите начать заново, нажмите 'Начать обучение'.", reply_markup=main_menu)

# Асинхронный запуск с использованием asyncio
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
