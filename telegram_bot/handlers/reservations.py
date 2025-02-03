from aiogram import types
from aiogram.client.session import aiohttp
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import ClientSession
from services.api_client import handle_api_response
from bot_config import API_LINK


async def cmd_book(message: Message):
    try:
        event_id = int(message.text.split()[1])
        user_id = message.from_user.id

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{API_LINK}/reservation/", json={"user_id": user_id, "event_id": event_id}
            ) as response:
                data = await response.json()

                if response.status == 201:
                    reservation_id = data["data"]["id"]
                    await message.reply(f"✅ Бронирование #{reservation_id} успешно создано!")
                else:
                    error_detail = data.get("detail", "Unknown error")
                    await message.reply(f"❌ Ошибка: {error_detail}")

    except (IndexError, ValueError):
        await message.reply("ℹ️ Формат команды: /book <ID_мероприятия>\nПример: /book 5")
    except Exception as e:
        await message.reply("🚧 Произошла внутренняя ошибка сервера")


async def cmd_my_reservations(message: Message):
    user_id = message.from_user.id

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_LINK}/reservation/user/{user_id}") as response:
            data = await response.json()

            if response.status == 200:
                reservations = data["data"]
                if reservations:
                    res_list = "\n".join(
                        [f"🎫 #{res['id']}: Мероприятие {res['event_id']} ({res['status']})" for res in reservations]
                    )
                    await message.reply(f"📖 Ваши бронирования:\n{res_list}")
                else:
                    await message.reply("📭 У вас нет активных бронирований")
            else:
                error_detail = data.get("detail", "Unknown error")
                await message.reply(f"❌ Ошибка: {error_detail}")


async def cmd_cancel(message: Message):
    try:
        reservation_id = int(message.text.split()[1])
        user_id = message.from_user.id

        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{API_LINK}/reservation/{reservation_id}", json={"user_id": user_id}
            ) as response:
                if response.status == 204:
                    await message.reply(f"✅ Бронирование #{reservation_id} успешно отменено!")
                else:
                    data = await response.json()
                    error_detail = data.get("detail", "Unknown error")
                    await message.reply(f"❌ Ошибка: {error_detail}")

    except (IndexError, ValueError):
        await message.reply("ℹ️ Формат команды: /cancel <ID_бронирования>\nПример: /cancel 12")
    except Exception as e:
        await message.reply("🚧 Произошла внутренняя ошибка сервера")


async def cmd_event_reservations(message: Message):
    try:
        event_id = int(message.text.split()[1])
        user_id = message.from_user.id

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{API_LINK}/reservation/event/{event_id}/reservations",
                params={"user_id": user_id, "event_id": event_id},
            ) as response:
                data = await response.json()

                if response.status == 200:
                    reservations = data["data"]
                    if reservations:
                        res_list = "\n".join(
                            [f"🎟️ #{res['id']}: Пользователь {res['user_id']} ({res['status']})" for res in reservations]
                        )
                        await message.reply(f"📊 Бронирования мероприятия #{event_id}:\n{res_list}")
                    else:
                        await message.reply("📭 На это мероприятие нет бронирований")
                else:
                    error_detail = data.get("detail", "Unknown error")
                    await message.reply(f"❌ Ошибка: {error_detail}")

    except (IndexError, ValueError):
        await message.reply("ℹ️ Формат команды: /event_reservations <ID_мероприятия>\nПример: /event_reservations 5")
    except Exception as e:
        await message.reply("🚧 Произошла внутренняя ошибка сервера")


def format_reservations(reservations):
    if not reservations:
        return "📭 У вас нет активных бронирований"
    return "📖 Ваши бронирования:\n" + "\n".join(
        f"🎫 #{res['id']}: Мероприятие {res['event_id']} ({res['status']})" for res in reservations
    )
