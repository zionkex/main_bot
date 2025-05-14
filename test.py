import asyncio
from sqlalchemy.ext.asyncio import AsyncSession


from database.engine import db2
from database.orm_queries import get_work_bot, get_user_by_tg_id, get_worker_info

async def main():
    async with db2.sessionmaker() as session:

        profits = await get_worker_info(session=session, telegram_id=5948265790)
        print(profits.profit_balance)

if __name__ == "__main__":
    asyncio.run(main())