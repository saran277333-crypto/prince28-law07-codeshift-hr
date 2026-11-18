import asyncio

from sqlalchemy import text

from codeshift_hr.db.session import engine


async def main():
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT version()"))
        print("Connected successfully!")
        print(result.scalar())

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
