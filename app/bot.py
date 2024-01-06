import os
import cv2
import numpy as np
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

import database as db
from run_model import model_evaluate


load_dotenv()
bot = Bot(os.getenv('TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot)


async def on_startup(_):
    await db.db_start()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer('Загрузите изображение')
    await db.cmd_start_db(message.from_user.id)


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


def get_text(emotion_class):
    if emotion_class == 1:
        return 'Настроение отрицательное'
    elif emotion_class == 0:
        return 'Настроение положительное'
    else:
        return 'Лицо не распознано, попробуйте снова'


# @dp.message_handler(text='Проверить состояние депозитов')
# async def answer(message: types.Message):
#     user_id = message.from_user.id
#     user_wallets = data.users_wallets.get(message.from_user.id, None)
#     if user_wallets:
#         await message.answer(await data.wallet_info(data.balances, data.users_wallets[user_id]),
#                              reply_markup=kb.wallet_status)
#     else:
#         await message.answer('Кошельки не найдены', reply_markup=kb.wallet_status)
#
#
# @dp.message_handler(text='Текущее состояние пулов Connext')
# async def first(message: types.Message):
#     await message.answer(await data.pool_info(data.balances),
#                          reply_markup=kb.main)
#
#
# @dp.message_handler(Wallet_Check())
# async def check_wallet(message: types.Message) -> None:
#     user_id = message.from_user.id
#     addresses = message.text.lower().split('\n')
#     if data.users_wallets.get(user_id, None):
#         data.users_wallets[user_id].extend(addresses)
#     else:
#         data.users_wallets[user_id] = addresses
#
#     with open("users_wallets.json", "w", encoding="utf-8") as file:
#         json.dump(data.users_wallets, file)
#
#     await message.reply(await data.wallet_info(data.balances, data.users_wallets[user_id]),
#                         reply_markup=kb.wallet_status)
#
#
# @dp.message_handler()
# async def check_wallet(message: types.Message) -> None:
#     await message.reply('Не понял')
#
#
# @dp.callback_query_handler()
# async def callback_query_keyboard(callback_query: types.CallbackQuery):
#     if callback_query.data == 'add_wallet':
#         await bot.send_message(chat_id=callback_query.from_user.id, text='Введите адрес(а)')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
