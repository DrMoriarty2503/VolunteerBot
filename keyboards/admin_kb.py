from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,InlineKeyboardMarkup, InlineKeyboardButton

send_tokens=KeyboardButton("/send")
send_keyboard=ReplyKeyboardMarkup(resize_keyboard=True)
send_keyboard.row(send_tokens)

inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="Одобрить", callback_data='yes'))