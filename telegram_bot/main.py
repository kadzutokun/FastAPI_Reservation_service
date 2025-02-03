import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from telegram_bot.bot_config import TOKEN
from telegram_bot.handlers import (
    common,
    events,
    reservations,
    users
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()


def register_handlers():
    dp.message.register(common.cmd_start, CommandStart())

    dp.message.register(reservations.cmd_book, Command("book"))
    dp.message.register(reservations.cmd_my_reservations, Command("my_reservations"))
    dp.message.register(reservations.cmd_event_reservations, Command("event_reservations"))
    dp.message.register(reservations.cmd_cancel, Command("cancel"))

    dp.message.register(events.cmd_create_event, Command("create_event"))
    dp.message.register(events.cmd_update_event, Command("update_event"))
    dp.message.register(events.cmd_get_event, Command("get_event"))
    dp.message.register(events.cmd_search_events, Command("search_event"))

    dp.message.register(users.cmd_register, Command("register"))
    dp.message.register(users.cmd_profile, Command("profile"))


async def main():
    register_handlers()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")