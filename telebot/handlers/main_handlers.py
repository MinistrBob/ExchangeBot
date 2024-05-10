from aiogram.types import Message


async def ping(message: Message):
    await message.answer("pong")
