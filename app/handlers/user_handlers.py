from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

import os

from states.user_states import EditPost
from core.init_bot import bot
from ai_generator import generate_post_text
from keyboards.user_kbs import edit_kb, get_channels
from config import MY_CHANNELS_IDS


user_router = Router()

load_dotenv()


@user_router.message(CommandStart())
async def start_handler(message: Message):
    if message.from_user.id != int(os.getenv('ADMIN_CHAT_ID')):
        return
    await message.answer('Добро пожаловать бота стилера контента. Не желательно удалять контент, который был сгенерирован ботом.')


@user_router.callback_query(F.data == 'regenerate')
async def additional_data(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    info_message = await callback.message.answer('Введите дополнительные данные')
    
    post_text = callback.message.text or callback.message.caption
    await state.update_data({'post_text': post_text,
                                'message_id':callback.message.message_id, 
                                'info_message_id':info_message.message_id, 
                                'photo':callback.message.photo, 
                                'video':callback.message.video})
    await state.set_state(EditPost.additional_data)


@user_router.message(EditPost.additional_data)
async def regenerate_handler(message: Message, state: FSMContext):
    if message.content_type != ContentType.TEXT:
        await message.answer('Введите текст')
        return
    
    waiting_message = await message.answer('Генерирую...')
    
    data = await state.get_data()
    answer_text = await generate_post_text(before_text=data['post_text'], additional_data=message.text)

    if answer_text == 'Ошибка':
        await message.answer('Ошибка')
    elif data['photo'] is None and data['video'] is None:
        await bot.edit_message_text(chat_id=message.chat.id,
                                    message_id=data['message_id'], 
                                    text=answer_text, reply_markup=edit_kb,
                                    parse_mode=ParseMode.MARKDOWN)
    else:
        await bot.edit_message_caption(chat_id=message.chat.id, 
                                        message_id=data['message_id'],
                                        caption=answer_text, 
                                        reply_markup=edit_kb,
                                        parse_mode=ParseMode.MARKDOWN)
    
    await waiting_message.delete() 
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=data['info_message_id'])
    
    await state.clear() 


@user_router.callback_query(F.data == 'delete_media')
async def delete_media_handler(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.answer(callback.message.caption, reply_markup=callback.message.reply_markup)
        await callback.message.delete()
    except:
        await callback.message.answer('Ошибка, скорее всего это не медиа')


@user_router.callback_query(F.data == 'post')
async def post_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.answer('Выберите канал', reply_markup=get_channels())
    
    content = callback.message.text or callback.message.caption or None
    await state.update_data({'photo':callback.message.photo,
                                'content':content, 
                                'video':callback.message.video})


@user_router.callback_query(F.data.startswith('ch_post_'))
async def posting(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    channel_id = int(MY_CHANNELS_IDS[callback.data.split('_')[-1]])
    
    data = await state.get_data()
    if data['photo'] is not None:
        await bot.send_photo(chat_id=channel_id, 
                                photo=data['photo'][-1].file_id,
                                caption=data['content'],
                                parse_mode=ParseMode.MARKDOWN)
    elif data['video'] is not None:
        await bot.send_video(chat_id=channel_id, 
                                video=data['video'].file_id, 
                                caption=data['content'],
                                parse_mode=ParseMode.MARKDOWN)
    else:
        await bot.send_message(chat_id=channel_id, 
                                text=data['content'],
                                parse_mode=ParseMode.MARKDOWN)

    await callback.message.delete()
    await state.clear()

