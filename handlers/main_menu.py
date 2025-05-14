from aiogram import Router,F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.orm_queries import get_work_bot
from handlers.commands import show_profile
from keyboards.inline import inline_keyboard
from keyboards.reply import main_menu
from utils.menu_enum import MainMenuEnum
from sqlalchemy.ext.asyncio import AsyncSession
main_menu_router = Router()


@main_menu_router.message(F.text==MainMenuEnum.PROFILE.value)
async def profile_menu(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await show_profile(event=message, state=state, session=session)


@main_menu_router.message(F.text==MainMenuEnum.ABOUT_PROJECT.value)
async def about_project(message: Message) -> None:
    await message.answer(
        "🔹 Дата открытия - 30.04.25\n"
        " ┠  Выплаты производятся в USDT на CryptoBot (https://t.me/send)\n"
        " ┖  Курс выплат - Bybit (https://www.bybit.com/ru-RU/convert/rub-to-usdt/)\n\n"
        "🔸 Проценты выплат:\n"
        " ┠ Пополнение/прямой - 85%\n"
        " ┠ ТП - 75%\n"
        " ┖ Прозвон - 65%\n\n"
        "👁‍🗨 Статус сервисов:\n"
        " ┠ TRADE  - ✅\n"
        " ┠ NFT - ✅\n"
        " ┠ ESCORT - ✅\n"
        " ┖ Прямые переводы - ✅\n\n"
        "⚡️ По всем вопросам - AnswerMT (https://t.me/AnswerMT)\n"
        " ┖ Канал обновлений проекта (https://t.me/+aomBDIzRDxVkNDAy)",
        disable_web_page_preview=True,
        reply_markup=main_menu()
    )

@main_menu_router.message(F.text==MainMenuEnum.INFORMATION.value)
async def information(message: Message) -> None:
    await message.answer(
        "💸 Общая касса проекта за все время - 1316648 RUB\n"
        "┖ Количество профитов - 87\n\n"
        "‼️ Администрация проекта никогда не будет писать вам с просьбами занять денег, сверяйте username.\n"
        "┖ Список администрации (https://t.me/c/1731858358/564)\n"
        "┖ Правила проекта (https://t.me/rulesMT)\n\n"
        "🔆 Выплаты профитов приходят в течение 24 часов в Work бота. Блокировки также подлежат выплате.\n\n"
        "💳 Нужны реквизиты для большого перевода? - Major Finance (https://t.me/FinanceMT)\n\n"
        "⚠️ Обнаружили баг или уязвимость?\n"
        "┖ Feedback (https://t.me/FeedbackTMBot)"
    )

@main_menu_router.message(F.text==MainMenuEnum.SHOP.value)
async def nft(message: Message,session:AsyncSession) -> None:
    bots= await get_work_bot(session=session,type = 'rest')
    await message.answer("🖥 Активные боты для работы:",
        reply_markup=inline_keyboard(bots=bots)
    )   