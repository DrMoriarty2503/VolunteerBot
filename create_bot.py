from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pyqiwip2p import QiwiP2P
import random
storage=MemoryStorage()

bot = Bot(token='5445080094:AAFh66B9_oKDRyXOtk0AZ59OF1dc59ISv0I')
dp=Dispatcher(bot, storage=storage)
p2p = QiwiP2P(auth_key='eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjZlbXBjbS0wMCIsInVzZXJfaWQiOiI3OTc3NjY4MDI0NSIsInNlY3JldCI6ImJhNDBlZDYwNWM3ZjY3ZTI0NmE1NmM1ZGEzYzAwNjE1ZmJkNTNlNzlmMDg2ZjNmM2E2ZGQ2MGM3Mzk4MDFjNjUifX0=')

