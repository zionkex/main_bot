import asyncio
from database.engine import db2
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from database.orm_queries import get_work_bot


async def main():
    
    async with db2.sessionmaker() as session:
        users = await session.execute(select(User))
        for user in users.scalars().all():
            print(user.telegram_name)

if __name__ == "__main__":
    asyncio.run(main())