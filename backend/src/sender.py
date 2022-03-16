import aiohttp
from config import logger, TOKEN, ADMIN_IDS
from src.storage import storage, lock


async def send_to_bot(text: str):
    logger.error(text)
    async with aiohttp.ClientSession() as session:
        for user_id in ADMIN_IDS:
            async with session.get(
                f'https://api.telegram.org/bot{TOKEN}/sendMessage',
                params={
                    'chat_id': user_id,
                    'text': text
                }
            ) as response:
                if not response.ok:
                    logger.error(f'MESSAGE NOT WAS SENT: {text}. {await response.text()}')


async def send_report(title: str, url: str, message: str, tag: str, is_error: bool):
    async with lock:
        if is_error:
            await storage.add_error(title)
        else:
            await storage.remove_error(title)
        statuses = await storage.get_text()
        symbol = '🟢' if len(statuses) == 0 else '🔴'
        text = (
            f'{symbol} (#{tag}) {title}\n'
            f'{message}\n'
            f'URL: {url}\n'
            f'\n'
            f'{statuses}'
        )
    await send_to_bot(text)
