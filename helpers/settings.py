# (c) @AbirHasan2005

import asyncio
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, MessageNotModified

from helpers.database.access_db import db


async def ShowSettings(event: Message, user_id: int):
    """
    Hiển thị bảng cài đặt tùy chỉnh với dữ liệu cập nhật.

    :param event: Chuyển đối tượng Tin nhắn có thể chỉnh sửa.
    :param user_id: Chuyển User ID để lấy dữ liệu của người dùng đó.
    """

    service_on = await db.get_service_on(user_id)
    footer_ = await db.get_footer_text(user_id)
    # Bug >>>
    also_footer2text = await db.get_add_text_footer(user_id)
    also_footer2photo = await db.get_add_photo_footer(user_id)
    channel_id = await db.get_channel_id(user_id)
    markup = [
        [InlineKeyboardButton(f"Bot đang {'BẬT' if (service_on is True) else 'TẮT'} ✅", callback_data="triggerService")],
        [InlineKeyboardButton("Đặt văn bản chân trang", callback_data="setFooterText")],
        [InlineKeyboardButton(f"Cũng áp dụng chân trang cho ảnh - {'BẬT' if (also_footer2text is True) else 'TẮT'} ✅", callback_data="setAlsoFooter2Text")],
        [InlineKeyboardButton(f"Cũng áp dụng chân trang cho văn bản - {'BẬT' if (also_footer2photo is True) else 'TẮT'} ✅", callback_data="setAlsoFooter2Photo")]
    ]
    # Bug <<<
    if footer_ is not None:
        markup.append([InlineKeyboardButton("Xóa văn bản chân trang", callback_data="rmFooterText"),
                       InlineKeyboardButton("Hiển thị Văn bản Chân trang", callback_data="showFooterText")])
    if channel_id is None:
        markup.append([InlineKeyboardButton("Đặt ID kênh", callback_data="setChannelID")])
    else:
        markup.append([InlineKeyboardButton("Thay đổi ID kênh", callback_data="setChannelID")])
    try:
        await event.edit(
            text="Tại đây Bạn có thể đặt cài đặt của mình:",
            reply_markup=InlineKeyboardMarkup(markup)
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await ShowSettings(event, user_id)
    except MessageNotModified:
        pass
