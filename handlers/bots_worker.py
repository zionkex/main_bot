from datetime import datetime, timezone
from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from callbacks import BotWorker
from database.orm_queries import change_user_to_worker, get_bot_by_nickname, update_worker
from handlers.commands import show_profile
from keyboards.inline import back_profile_kb, keyboard_workerbot
from database.engine import db2
from utils.user_url import get_user_link_html

class UserState(StatesGroup):
    main_menu = State()
    change_tag = State()
    change_wallet = State()
    send_check = State()


bot_worker_router = Router()

@bot_worker_router.message(UserState.change_tag)
async def change_tag(message: Message, state: FSMContext, session: AsyncSession) -> None:
    new_tag = message.text
    async with db2.sessionmaker() as session:
        await update_worker(session=session, telegram_id=message.from_user.id, tag=new_tag)    
    await message.answer("✅ Тег успешно изменен")
    await show_profile(event=message, state=state, session=session)
    await state.set_state(UserState.main_menu)

@bot_worker_router.message(UserState.change_wallet)
async def change_wallet(message: Message, state: FSMContext, session: AsyncSession) -> None:
    new_wallet = message.text
    async with db2.sessionmaker() as session:
        await update_worker(session=session, telegram_id=message.from_user.id, crypto_wallet=new_wallet)    
    await message.answer("✅ Кошелек успешно изменен")
    await show_profile(event=message, state=state, session=session)
    await state.set_state(UserState.main_menu)

@bot_worker_router.message(UserState.send_check)
async def send_check(message: Message) -> None:
    if message.photo:
        file_id = message.photo[-1].file_id
        await message.bot.send_photo(chat_id=5948265790,
        caption=f"Чек от {get_user_link_html(user=message.from_user)}",photo=file_id)
        await message.answer("✅ Чек успешно отправлен на проверку",reply_markup=back_profile_kb())
    await message.answer("❌ Ошибка, попробуйте еще раз",reply_markup=back_profile_kb())

@bot_worker_router.callback_query(BotWorker.filter())
async def bot_worker(callback: CallbackQuery, callback_data: BotWorker, session: AsyncSession,state:FSMContext) -> None:
    if callback_data.action == 'get_info':
        bot = await get_bot_by_nickname(session=session, nickname=callback_data.bot_username)
        if callback_data.type == 'rest':
            text = (
                f"💊 Отдых ({bot.name})\n\n"
                "🤖 Бот для работы:\n"
                f"╰•<a href='https://t.me/{bot.nickname}'>{bot.name}</a>\n\n"
                "📜 Мануал:\n"
                "╰•<a href='https://teletype.in/@enigmateam/A86FecA-8-P'>Читать</a>\n\n"
                "🔗 Ваша реферальная ссылка:\n"
                f"╰• https://t.me/{bot.nickname}?start={callback.from_user.id}\n\n"
            )
        
            user_data = {
                "telegram_name": callback.from_user.full_name,
                "telegram_username": callback.from_user.username,
                "join_date": datetime.now(timezone.utc),
                "last_activity": datetime.now(timezone.utc),
            }
            async with db2.sessionmaker() as session:
                await change_user_to_worker(session=session, user_id=callback.from_user.id, user_data=user_data)
            await callback.message.edit_text(text=text, disable_web_page_preview=True
                                             ,reply_markup=keyboard_workerbot(bot_username=bot.nickname
                                                                                     ,user_id=callback.from_user.id))
            
    elif callback_data.action == 'hide_ref_link':
        await callback.bot.send_message(chat_id=callback.from_user.id,
                                             text=f"<a href='https://t.me/{callback_data.bot_username}?start={callback.from_user.id}\'>@{callback_data.bot_username}</a>",)
    
    elif callback_data.action == 'change_tag':
        text="#️⃣ Введите ваш новый тег:"
        await state.set_state(UserState.change_tag)
        await callback.message.edit_text(text=text,reply_markup=back_profile_kb())

    elif callback_data.action == 'change_wallet':
        text="💰 Введите ваш новый кошелек:"
        await state.set_state(UserState.change_wallet)
        await callback.message.edit_text(text=text,reply_markup=back_profile_kb())

    elif callback_data.action == 'send_check':
        text="🧾 Отправьте чек на проверку"
        await callback.message.edit_text(text=text,reply_markup=back_profile_kb())
        await state.set_state(UserState.send_check)

    elif callback_data.action == 'back_profile':
        await show_profile(event=callback, state=state, session=session)
    await callback.answer()