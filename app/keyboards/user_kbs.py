from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import MY_CHANNELS_IDS


edit_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Regenerate', callback_data='regenerate'),
        InlineKeyboardButton(text='Delete Media', callback_data='delete_media')],
    [InlineKeyboardButton(text='Post', callback_data='post')]
])

def get_channels():
    btns = [InlineKeyboardButton(text=username, callback_data=f'ch_post_{username}') for username in MY_CHANNELS_IDS]
    return InlineKeyboardMarkup(inline_keyboard=[
        btns
    ])