from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import my_channels_ids


edit_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Regenerate', callback_data='regenerate'),
        InlineKeyboardButton(text='Delete Photo', callback_data='delete_photo')],
    [InlineKeyboardButton(text='Post', callback_data='post')]
])

def get_channels():
    btns = [InlineKeyboardButton(text=username, callback_data=f'ch_post_{username}') for username in my_channels_ids]
    return InlineKeyboardMarkup(inline_keyboard=[
        btns
    ])