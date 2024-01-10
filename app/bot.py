import os
import cv2
import numpy as np
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

import database as db
import keyboard as kb
from run_model import model_evaluate
from utils import get_text, emotion_history_text


load_dotenv()
bot = Bot(os.getenv('TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot)


async def on_startup(_):
    await db.db_start()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(
        f'Привет, {message.from_user.first_name}!\n'
        f'Загрузите изображение для проверки настроения',
        reply_markup=kb.main
    )
    await db.cmd_start_db(message.from_user.id)


@dp.message_handler(text='Проверить настроение')
async def check_emotion(message: types.Message):
    await message.answer('Загрузите изображение')


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def emotion_recognition(message: types.Message):
    photo = message.photo[-1]
    photo_bytes = await bot.download_file_by_id(photo.file_id)

    np_array = np.frombuffer(photo_bytes.getvalue(), np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    emotion_class = await model_evaluate(image)
    emotion_map = {0: 'positive', 1: 'negative'}

    await message.answer(get_text(emotion_class))
    if emotion_class is not None:
        print(emotion_class)
        await db.extend_emotion(message.from_user.id, emotion_map[emotion_class])


@dp.message_handler(text='История наблюдений')
async def emotion_history(message: types.Message):
    emotion_info = await db.emotion_history(message.from_user.id)
    await message.answer(
        f'{emotion_history_text(emotion_info)}\n'
        f'Вывести историю за последние:',
        reply_markup=kb.emotion_history
    )


@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery):
    history = await db.emotion_history(callback_query.from_user.id, callback_query.data)
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=emotion_history_text(history, callback_query.data)
    )


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
