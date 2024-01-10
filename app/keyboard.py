from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Проверить настроение').add('История наблюдений')

emotion_history = InlineKeyboardMarkup(row_width=1)
emotion_history.add(InlineKeyboardButton(text="7 дней", callback_data='7 days'))
emotion_history.add(InlineKeyboardButton(text="30 дней", callback_data='1 month'))
