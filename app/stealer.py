from telethon import TelegramClient, events
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import BufferedInputFile
from dotenv import load_dotenv

from typing import Union
import os
import logging

from core.init_bot import bot as bot_aiogram
from ai_generator import generate_post_text
from keyboards.user_kbs import edit_kb
from config import WATCHED_CHANNELS


load_dotenv()


API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')


telethon_client = TelegramClient(
    'telethon_session',
    API_ID,
    API_HASH,
    system_version='ANDROID 14',
    device_model='poco f6'
)


async def send_to_admin(text: Union[str, None], photo: bytes = None, video: bytes = None):
    if photo:
        file = BufferedInputFile(photo, filename='image.jpg')
        answer_text = await generate_post_text(text) if text else ''
        await bot_aiogram.send_photo(ADMIN_CHAT_ID, 
                                        photo=file, 
                                        caption=answer_text, 
                                        reply_markup=edit_kb, 
                                        parse_mode=ParseMode.MARKDOWN)
    elif video:
        answer_text = await generate_post_text(text) if text else ''
        file = BufferedInputFile(video, filename='video.mp4')
        await bot_aiogram.send_video(ADMIN_CHAT_ID, 
                                        video=file,
                                        caption=answer_text, 
                                        reply_markup=edit_kb,
                                        parse_mode=ParseMode.MARKDOWN)
    else:
        answer_text = await generate_post_text(text) if text else ''
        await bot_aiogram.send_message(ADMIN_CHAT_ID,
                                        text=answer_text, 
                                        reply_markup=edit_kb,
                                        parse_mode=ParseMode.MARKDOWN)


@telethon_client.on(events.NewMessage(chats=WATCHED_CHANNELS))
async def handler(event):
    message = event.message

    if hasattr(message, 'grouped_id') and message.grouped_id is not None:
        return

    photo_bytes = None
    video_bytes = None

    if message.photo:
        photo_bytes = await telethon_client.download_media(message.photo, bytes)
    elif message.video:
        video_bytes = await telethon_client.download_media(message.video, bytes)

    text = message.text if message.text else None

    await send_to_admin(text=text, photo=photo_bytes, video=video_bytes)


async def main():
    await telethon_client.start()
    logging.info('Telethon client started')
    await telethon_client.run_until_disconnected()
