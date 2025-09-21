import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random
import os
import asyncio

API_TOKEN = os.getenv('API_TOKEN')  # API токен будет храниться в переменной окружения Railway

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

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
    # добавьте все остальные шаги из вашего кода
]

# Вопросы для викторины
quiz_questions = [
    {"question": "Какой счет идет в теннисе после 30-30?", "options": ["40-30", "15-30", "40-40"], "answer": "40-30"},
    # добавьте остальные вопросы
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

# Запуск бота с использованием asyncio
async def main():
    await dp.start_polling()

if __name__ == '__main__':
    # Запуск бота с asyncio
    asyncio.run(main())
