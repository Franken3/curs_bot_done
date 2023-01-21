from aiogram.dispatcher.filters.state import StatesGroup, State

class UserState(StatesGroup):
    currency_state = State()
    currency_state_confirm = State()
    push_state = State()