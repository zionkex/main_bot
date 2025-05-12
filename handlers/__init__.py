from aiogram import Router
from handlers.commands import command_router
from handlers.main_menu import main_menu_router
from handlers.bots_worker import bot_worker_router

main_router = Router()
main_router.include_routers(main_menu_router,bot_worker_router,command_router)