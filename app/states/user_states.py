from aiogram.fsm.state import StatesGroup, State


class EditPost(StatesGroup):
    additional_data = State()