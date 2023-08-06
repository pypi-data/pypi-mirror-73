import asyncio
from .environment import NODE


async def main():
    await NODE.run()


if __name__ == "__main__":
    asyncio.run(main())
