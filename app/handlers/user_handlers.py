from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import Command, CommandStart

from core.init_bot import bot


user_router = Router()


@user_router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer('Добро пожаловать бота стилера контента')