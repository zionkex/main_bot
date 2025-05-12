from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from callbacks import BotWorker
from database.orm_queries import get_bot_by_nickname
from keyboards.inline import inline_keyboard_workerbot

bot_worker_router = Router()

@bot_worker_router.callback_query(BotWorker.filter())
async def bot_worker(callback: CallbackQuery, callback_data: BotWorker, session: AsyncSession) -> None:
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
            await callback.message.edit_text(text=text, disable_web_page_preview=True
                                             ,reply_markup=inline_keyboard_workerbot(bot_username=bot.nickname
                                                                                     ,user_id=callback.from_user.id,
                                                                                     bot_type=bot.type))
            
    elif callback_data.action == 'hide_ref_link':
        await callback.bot.send_message(chat_id=callback.from_user.id,
                                             text=f"<a href='https://t.me/{callback_data.bot_username}?start={callback.from_user.id}\'>@{callback_data.bot_username}</a>",)
    
    await callback.answer()