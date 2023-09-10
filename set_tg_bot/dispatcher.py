from aiogram import Dispatcher
from .bot import my_bot
from set_tg_bot.memory import my_memory


my_disp = Dispatcher(bot=my_bot, storage=my_memory)
