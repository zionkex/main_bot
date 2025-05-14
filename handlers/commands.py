from datetime import datetime
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message,CallbackQuery
from database.orm_queries import get_worker_info
from keyboards.inline import profile_kb
from utils.bot_state import UserState
from keyboards.reply import main_menu
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
from database.engine import db2
from utils.menu_enum import MainMenuEnum
command_router = Router()

async def show_profile(event: Message|CallbackQuery, state: FSMContext, session: AsyncSession,) -> None:
    async with db2.sessionmaker() as session:
        worker = await get_worker_info(session=session, telegram_id=event.from_user.id)
        text=("<b>💼 Профиль</b>\n"
                         f"┣ ID: ({event.from_user.id})\n"
                         f"┣ Username: @{event.from_user.username if event.from_user.username else "отсуствует"}\n"
                         "┗ Ранг: Low\n\n"
                         "〽️ <b>Личная статистика</b>\n"
                         f"┣ Сумма профитов: {worker.profit_balance} RUB\n"
                         f"┗ Количество профитов: {worker.profit_count}\n\n"
                         "<b>🎭 Информация\n</b>"
                         f"┣ Тег в выплатах: <b>{f'#{worker.tag}' if worker.tag else 'отсуствует'}</b>\n"
                         f'┣ Кошелек: <b>{worker.crypto_wallet if worker.crypto_wallet else "отсуствует"}</b>\n'
                         "┣ Статус: Воркер\n"
                         f"┗ В команде: {(datetime.now().date() - worker.join_date.date()).days} дней\n")
                        
    if isinstance(event, Message):
        await event.answer(text=text,reply_markup=profile_kb())
    else:
        await event.message.edit_text(text=text,reply_markup=profile_kb())
    await state.set_state(UserState.main_menu)

@command_router.message(CommandStart())
async def cmd_start(message: Message,state:FSMContext,session:AsyncSession) -> None:
    await message.answer_sticker("CAACAgIAAxkBAAEObXhoG31-0ExU21Op-Uq0Fge3hyvJNgACOXMAAlJGGEvAgeYEhpsRcDYE",
                                 reply_markup=main_menu())
    await show_profile(event=message, state=state, session=session)
