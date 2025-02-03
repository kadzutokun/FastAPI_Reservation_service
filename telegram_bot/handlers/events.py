from datetime import datetime

from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import ClientSession
from bot_config import API_LINK
from services.api_client import handle_api_response


async def cmd_create_event(message: Message):
    try:
        # Парсинг аргументов из сообщения
        args = message.text.split()[1:]
        if len(args) < 4:
            raise ValueError

        title = args[0]
        description = args[1]
        date = args[2]
        seats = int(args[3])

        datetime.strptime(date, "%Y-%m-%d")

        async with ClientSession() as session:
            response = await session.post(
                f"http://{API_LINK}:8000/events/create",
                json={
                    "title": title,
                    "description": description,
                    "date": date,
                    "available_seats": seats,
                    "user_id": message.from_user.id,
                },
            )
            return await handle_api_response(
                response,
                message,
                success_msg=f"✅ Мероприятие '{title}' успешно создано!",
                error_prefix="Создание мероприятия",
            )
    except ValueError:
        await message.reply(
            "ℹ️ Формат команды:\n"
            "/create_event <Название> <Описание> <Дата(YYYY-MM-DD)> <Количество мест>\n\n"
            "Пример:\n"
            "/create_event КонференцияIT 'IT-конференция' 2024-12-15 100"
        )
    except Exception as e:
        await message.reply(f"🚧 Ошибка: {str(e)}")


async def cmd_update_event(message: Message):
    try:
        args = message.text.split()[1:]
        if len(args) < 2:
            raise ValueError

        event_id = int(args[0])
        update_data = {}

        # Парсинг параметров обновления
        for param in args[1:]:
            if "=" in param:
                key, value = param.split("=", 1)
                key = key.strip().lower()

                if key == "seats":
                    update_data["available_seats"] = int(value)
                elif key == "title":
                    update_data["title"] = value
                elif key == "description":
                    update_data["description"] = value
                elif key == "date":
                    datetime.strptime(value, "%Y-%m-%d")
                    update_data["date"] = value

        if not update_data:
            raise ValueError("Нет параметров для обновления")

        async with ClientSession() as session:
            response = await session.patch(
                f"http://{API_LINK}:8000/events/{event_id}",
                json={"user_id": message.from_user.id, "event_id": event_id, **update_data},
            )
            return await handle_api_response(
                response,
                message,
                success_handler=lambda data: (
                    f"✅ Мероприятие обновлено!\n\n"
                    f"Новые данные:\n"
                    f"Название: {data['data']['title']}\n"
                    f"Описание: {data['data']['description']}\n"
                    f"Дата: {data['data']['date']}\n"
                    f"Мест: {data['data']['available_seats']}"
                ),
                error_prefix="Обновление мероприятия",
            )

    except ValueError as e:
        await message.reply(
            f"ℹ️ Формат команды:\n"
            f"/update_event <ID_мероприятия> [параметры]\n\n"
            f"Доступные параметры:\n"
            f"title=Новое название\n"
            f"description=Новое описание\n"
            f"date=2024-12-31\n"
            f"seats=50\n\n"
            f"Пример:\n"
            f"/update_event 15 title=НовоеНазвание seats=50"
        )
    except Exception as e:
        await message.reply(f"🚧 Ошибка: {str(e)}")


async def cmd_get_event(message: Message):
    try:
        event_id = int(message.text.split()[1])
        async with ClientSession() as session:
            response = await session.get(f"http://{API_LINK}:8000/events/{event_id}", params={"event_id": event_id})
            return await handle_api_response(
                response,
                message,
                success_handler=lambda data: (
                    f"📅 {data['data']['title']}\n\n"
                    f"Описание: {data['data']['description']}\n"
                    f"Дата: {data['data']['date']}\n"
                    f"Свободных мест: {data['data']['available_seats']}\n"
                    f"ID: {data['data']['id']}"
                ),
                error_prefix="Получение информации о мероприятии",
            )
    except (IndexError, ValueError):
        await message.reply("ℹ️ Формат команды: /event <ID_мероприятия>")


async def cmd_search_events(message: Message):
    try:
        search_query = message.text.split()[1]
        async with ClientSession() as session:
            response = await session.get(f"http://{API_LINK}:8000/events/", params={"title": search_query})
            return await handle_api_response(
                response,
                message,
                success_handler=lambda data: format_events_list(data["data"]),
                error_prefix="Поиск мероприятий",
            )
    except IndexError:
        await message.reply("ℹ️ Укажите поисковый запрос: /search_event <название>")


def format_events_list(events):
    if not events:
        return "🔍 Мероприятия не найдены"

    return "📅 Найденные мероприятия:\n\n" + "\n\n".join(
        f"{e['id']}. {e['title']}\n"
        f"Дата: {e['date']}\n"
        f"Свободных мест: {e['available_seats']}\n"
        f"Описание: {e['description'][:50]}..."
        for e in events
    )
