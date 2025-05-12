from aiogram.filters.callback_data import CallbackData

class MainMenu(CallbackData, prefix="main_menu"):
    action: str
    level: int

class BotWorker(CallbackData, prefix="bot_worker"):
    action: str
    bot_username: str|None= None
    type: str|None= None
