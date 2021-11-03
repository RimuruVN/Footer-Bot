# (c) @AbirHasan2005

import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait, MediaCaptionTooLong, MessageNotModified
from helpers.contact_user import NotifyUser


async def AddFooter(bot: Client, event: Message, text: str, user_id: int):
    """
    Chức năng trình chỉnh sửa phụ đề tùy chỉnh cho Footer Bot.

    :param bot: Vượt qua ứng dụng khách Bot.
    :param event: Vượt qua ứng dụng khách Bot.
    :param text: Chuyển đối tượng Tin nhắn.
    :param user_id: Chuyển user_id giống như on_event.
    """

    try:
        if event.text is None:
            await event.edit_caption(
                caption=f"{event.caption.markdown if (event.caption is not None) else ''}\n{text}",
                parse_mode="markdown"
            )
        else:
            await event.edit(
                text=f"{event.text.markdown}\n{text}",
                parse_mode="markdown"
            )
    except MediaCaptionTooLong:
        await NotifyUser(
            bot=bot,
            text=f"Không thể thêm văn bản chân trang vào [tin nhắn này](https://t.me/{'c/' + str(event.chat.id) + '/' + str(event.message_id) if (event.chat.username is None) else event.chat.username + '/' + str(event.chat.id) + '/' + str(event.message_id)}.\n\n**Lý do:** `Chú thích tin nhắn phương tiện quá dài!`",
            user_id=user_id
        )
        return
    except MessageNotModified:
        await NotifyUser(
            bot=bot,
            text=f"Không thể thêm văn bản chân trang vào [tin nhắn này](https://t.me/{'c/' + str(event.chat.id) + '/' + str(event.message_id) if (event.chat.username is None) else event.chat.username + '/' + str(event.chat.id) + '/' + str(event.message_id)}.\n\n**Lý do:** `Nhiều nút Trình chỉnh sửa Bots Chỉnh sửa Tin nhắn!`",
            user_id=user_id
        )
        return
    except FloodWait as e:
        if e.x > 180:
            await bot.leave_chat(chat_id=event.chat.id)
            await NotifyUser(
                bot=bot,
                text=f"Sorry.\nĐã nhận được 3 phút FloodWait từ `{str(event.chat.id)}` !!\n\nVì vậy, tôi đã rời khỏi Kênh đó.",
                user_id=user_id
            )
            await NotifyUser(
                bot=bot,
                text=f"Hello.\nĐã nhận được 3 phút FloodWait từ `{str(event.chat.id)}` !!\n\nVì vậy, tôi đã rời khỏi Kênh đó.",
                user_id=Config.BOT_OWNER
            )
            return
        print(f"Ngủ trong {e.x + 5}s - {event.chat.id} - @{event.chat.username}")
        await asyncio.sleep(e.x)
        await asyncio.sleep(5)
        await AddFooter(bot, event, text, user_id)
    except Exception as err:
        await NotifyUser(
            bot=bot,
            text=f"**Cảnh báo:** Tôi không thể thêm chân trang vào `{event.chat.id}`\n\n**Lý do:** `{err}`",
            user_id=Config.BOT_OWNER
        )
        return
