from aiogram.filters import CommandStart
from aiogram.types import Message

async def cmd_start(message: Message):
    await message.answer(
        "🎉 Добро пожаловать в бот управления мероприятиями!\n\n"
        
        "Если вы не зарегистрированы в системе, пожалуйста, воспользуйтесь командой /register\n\n"
        
        "Основные команды:\n"
        "/register <никнейм> - Регистрация\n"
        "/profile - Просмотр профиля\n\n"
        
        "/search_event <название> - Поиск мероприятий\n"
        "/book <id> - Бронирование\n"
        "/cancel <id мероприятия> - Отмена бронирования\n"
        "/get_event <id мероприятия> - Получение информации о мероприятии\n"
        "/my_reservations - Мои бронирования\n\n"
        
        "Для организаторов:\n"
        "/create_event - Создать мероприятие\n"
        "/update_event - Создать мероприятие\n"
        "/event_reservations <id> - Бронирования мероприятия"
    )