from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):
    main_menu = State()