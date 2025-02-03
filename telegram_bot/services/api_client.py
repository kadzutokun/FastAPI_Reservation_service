import logging
from aiogram.types import Message

logger = logging.getLogger(__name__)


async def handle_api_response(
        response,
        message: Message,
        success_msg: str = None,
        success_handler: callable = None,
        error_prefix: str = ""
):
    try:
        data = await response.json()

        if 200 <= response.status < 300:
            if success_handler:
                return await message.reply(success_handler(data['data']))
            return await message.reply(success_msg)

        error_detail = data.get('detail', 'Неизвестная ошибка')
        await message.reply(f"❌ {error_prefix}: {error_detail}")

    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        await message.reply("⚠️ Ошибка при обработке ответа сервера")