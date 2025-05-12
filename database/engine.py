from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import settings
from database.models import Base


class DatabaseConnecter:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        max_overflow: int = 10,
    ) -> None:
        self.url = url 
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            max_overflow=max_overflow,
        )
        self.sessionmaker : async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


db = DatabaseConnecter(
    url=settings.db.postgres_url,
    echo=settings.db.echo,
    max_overflow=settings.db.max_overflow,
)
async def create_db():
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

print(db.url,"first")

db2 = DatabaseConnecter(
    url=f"postgresql+asyncpg://{settings.db.postgres_user}:{settings.db.postgres_password}@{settings.db.postgres_host}:5434/octopus_russia",
    echo=settings.db.echo,
    max_overflow=settings.db.max_overflow,
)

print(db2.url,"second")
