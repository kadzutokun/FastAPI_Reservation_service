from aiogram import F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import ClientSession
from telegram_bot.services.api_client import handle_api_response
from telegram_bot.bot_config import API_LINK


async def cmd_register(message: Message):
    try:
        args = message.text.split()[1:]
        if len(args) < 1:
            raise ValueError

        nickname = ' '.join(args)
        telegram_id = str(message.from_user.id)

        async with ClientSession() as session:
            response = await session.post(
                f"{API_LINK}/users/register",
                json={
                    "telegram_id": telegram_id,
                    "nickname": nickname
                }
            )
            return await handle_api_response(
                response,
                message,
                success_handler=lambda data: (
                    f"✅ Регистрация успешна!\n\n"
                    f"Ваш профиль:\n"
                    f"ID: {data['data']['id']}\n"
                    f"Никнейм: {data['data']['nickname']}\n"
                    f"Telegram ID: {data['data']['telegram_id']}"
                ),
                error_prefix="Регистрация"
            )

    except ValueError:
        await message.reply("ℹ️ Формат команды: /register <никнейм>\nПример: /register Крутой_Айтишник")

async def cmd_profile(message: Message):
    try:
        user_id = message.from_user.id
        async with ClientSession() as session:
            response = await session.get(f"{API_LINK}/users/{user_id}")
            return await handle_api_response(
                response,
                message,
                success_handler=lambda data: format_profile(data['data']),
                error_prefix="Просмотр профиля"
            )
    except Exception as e:
        await message.reply(f"🚧 Ошибка: {str(e)}")


def format_profile(user_data):
    return (
        "👤 Профиль пользователя\n\n"
        f"ID: {user_data['id']}\n"
        f"Никнейм: {user_data['nickname']}\n"
        f"Telegram ID: {user_data['telegram_id']}\n"
    )
