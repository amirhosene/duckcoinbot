import pyrogram
from data import config
from utils.core import logger

async def create_sessions():
    while True:
        sessions_name = input("please inter name session:")
        if not sessions_name:
            return

        session = pyrogram.Client(api_id=config.API_ID, api_hash=config.API_HASH, name=sessions_name, workdir=config.WORKDIR)
        async with session:
            user_data = await session.get_me()

            logger.success(f'Session successful added for {user_data.username} | {user_data.phone_number}')