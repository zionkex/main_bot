from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

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

async def change_user_to_worker(session: AsyncSession, user_id: int,user_data:dict|None=None) -> None:
    result=await session.execute(
        select(User).where(User.telegram_id == user_id)
    )
    user = result.scalar_one_or_none()

    if user:
        if user.type != 'worker':
            user.type='worker'
    elif user is None:
        new_user = Worker(telegram_id=user_id, type='worker',**user_data)
        session.add(new_user)
    await session.commit()

async def get_user_by_tg_id(session: AsyncSession, tg_id: int) -> User:
    result = await session.execute(
        select(User).join(Worker,).where(User.telegram_id == tg_id)
    )
    user= result.scalars().first()


async def get_worker_info(session: AsyncSession, telegram_id: int):
    stmt = select(Worker).where(Worker.telegram_id == telegram_id)
    result = await session.execute(stmt)
    worker = result.scalar_one_or_none()

    if worker:
        return worker
    

async def update_worker(session: AsyncSession, telegram_id: int, **kwargs) -> None:
    stmt = select(Worker).where(Worker.telegram_id == telegram_id)
    result = await session.execute(stmt)
    worker = result.scalar_one_or_none()

    if worker:
        for key, value in kwargs.items():
            setattr(worker, key, value)
        await session.commit()
