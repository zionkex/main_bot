from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import Bot, User, Worker


async def get_work_bot(session: AsyncSession,type: str) -> Bot:
    result = await session.execute(
        select(Bot).where(Bot.type == type)
    )
    return result.scalars().all()

async def get_bot_by_nickname(session: AsyncSession, nickname: str) -> Bot:
    result = await session.execute(
        select(Bot).where(Bot.nickname == nickname)
    )
    return result.scalars().first()

async def change_user_to_worker(session: AsyncSession, user_id: int, bot_username: str) -> None:
    result=await session.execute(
        select(User).where(User.telegram_id == user_id)
    )
    user = result.scalars().first()

    if user:
        if user.type != 'worker':
            user.type='worker'
    else:
        new_user = Worker(telegram_id=user_id, type='worker', bot_username=bot_username)
        session.add(new_user)
    await session.commit()


