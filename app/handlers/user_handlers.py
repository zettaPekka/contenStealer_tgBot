from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from states.user_states import EditPost
from core.init_bot import bot
from ai_generator import generate_post_text
from keyboards.user_kbs import edit_kb, get_channels


user_router = Router()


@user_router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer('Добро пожаловать бота стилера контента')


@user_router.callback_query(F.data == 'regenerate')
async def additional_data(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    info_message = await callback.message.answer('Введите дополнительные данные')
    
    post_text = callback.message.text or callback.message.caption
    await state.update_data({'post_text': post_text, 'message_id':callback.message.message_id, 'info_message_id':info_message.message_id, 'photo':callback.message.photo})
    await state.set_state(EditPost.additional_data)


@user_router.message(EditPost.additional_data)
async def regenerate_handler(message: Message, state: FSMContext):
    waiting_message = await message.answer('Генерирую...')
    
    data = await state.get_data()
    answer_text = await generate_post_text(before_text=data['post_text'], additional_data=message.text)

    if data['photo'] is None:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=data['message_id'], text=answer_text, reply_markup=edit_kb)
    else:
        await bot.edit_message_caption(chat_id=message.chat.id, message_id=data['message_id'], caption=answer_text, reply_markup=edit_kb)
    await waiting_message.delete() 
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=data['info_message_id'])


@user_router.callback_query(F.data == 'delete_photo')
async def delete_photo_handler(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.answer(callback.message.caption, reply_markup=callback.message.reply_markup)
        await callback.message.delete()
    except:
        await callback.message.answer('Ошибка')


@user_router.callback_query(F.data == 'post')
async def post_handler(callback: CallbackQuery):
    await callback.answer()
    
    await callback.message.answer('Выберите канал', reply_markup=get_channels)


@user_router.callback_query(F.data.startswith('ch_post_'))
async def posting(callback: CallbackQuery):
    await callback.answer