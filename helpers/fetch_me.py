# (c) @AbirHasan2005

import asyncio
from pyrogram import Client
from pyrogram.errors import FloodWait
from helpers.contact_user import NotifyUser
from helpers.database.access_db import db


async def FetchMeOnChat(bot: Client, chat_id: int):
    try:
        FetchData = await bot.get_chat_member(chat_id=chat_id, user_id=(await bot.get_me()).id)
        return FetchData, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        if e.x > 60:
            await NotifyUser(
                bot,
                text=f"Bot bị lỗi FloodWait {str(e.x)} từ Trò chuyện của bạn: {str(chat_id)}\n\nVì vậy, dịch vụ hiện đã bị vô hiệu hóa!\nBạn có thể kích hoạt lại dịch vụ từ /settings !!",
                user_id=(await db.find_user_id(chat_id))
            )
        FetchData, err = await FetchMeOnChat(bot, chat_id)
        return FetchData, None
    except Exception as err:
        return 404, err
