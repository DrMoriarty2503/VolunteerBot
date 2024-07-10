from aiogram import types, Dispatcher
from create_bot import dp,bot
from keyboards import client_kb, admin_kb
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# ID=None
admin1_ID=1082853437


# async def admin_handlers(message: types.Message):
#     if message.text=="Отправить 5 токенов" and message.from_user.id==admin1_ID:
#         sqlite_db.cur.execute('INSERT INTO user_tokens VALUES(?,?)', (message.from_user.id,5))
#         sqlite_db.base.commit()
#
# def register_handlers_admin(dp: Dispatcher):
#     # dp.register_message_handler(start_commands,commands=['start','help'])
#     dp.register_message_handler(admin_handlers)

# class Price(StatesGroup):
#     choosing_price=State()
# @dp.message_handler(message.Text=='Отправить 5 токенов',state=None)
# async def cm_start(message: types.Message, state: FSMContext):
#     await Price.choosing_price.set()


