from aiogram.types import Message
import asyncio


async def ping(message: Message, bot: Bot):
    await message.answer("pong")
