# (c) @AbirHasan2005

import shutil
import psutil
import asyncio
from pyromod import listen
from asyncio import TimeoutError
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

from configs import Config
from helpers.database.access_db import db
from helpers.human_readable import humanbytes
from helpers.database.add_user import AddUserToDatabase
from helpers.settings import ShowSettings
from helpers.broadcast import broadcast_handler
from helpers.fetch_me import FetchMeOnChat
from helpers.add_footer import AddFooter

AHBot = Client(
    session_name=Config.SESSION_NAME,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)


@AHBot.on_message(filters.private & filters.command("start"))
async def _start(bot: Client, m: Message):
    await AddUserToDatabase(bot, m)
    try:
        await m.reply_text(
            Config.START_TEXT,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("OWOHUB 🔞", url="https://t.me/owohub"), InlineKeyboardButton("KÊNH SEX 🔞", url="https://t.me/kenhsex")],
                    [InlineKeyboardButton("Developer - @gimsuri", url="https://t.me/gimsuri")]
                ]
            ),
            quote=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await m.reply_text("Không có DDoS Plox!")


@AHBot.on_message(filters.private & filters.command("settings"))
async def _settings(bot: Client, event: Message):
    await AddUserToDatabase(bot, event)
    editable = await event.reply_text("Vui lòng chờ ...", quote=True)
    await ShowSettings(editable, user_id=event.from_user.id)


@AHBot.on_message(filters.channel & (filters.video | filters.document) & ~filters.edited & ~filters.private)
async def add_footer(bot: Client, event: Message):
    on_event = await db.find_user_id(event.chat.id)
    if on_event is None:
        return
    _I, _err = await FetchMeOnChat(bot, chat_id=event.chat.id)
    if _I == 404:
        print(f"Không thể chỉnh sửa tin nhắn trong {event.chat.id} !\nError: {_err}")
        return
    service_on = await db.get_service_on(int(on_event))
    footer_text = await db.get_footer_text(int(on_event))
    is_forward = event.forward_from_chat or event.forward_from
    if (_I.can_edit_messages is True) and (service_on is True) and (footer_text is not None) and (is_forward is None):
        await AddFooter(bot, event, footer_text, int(on_event))


@AHBot.on_message(filters.channel & filters.text & ~filters.edited & ~filters.private, group=-1)
async def add_text_footer(bot: Client, event: Message):
    on_event = await db.find_user_id(event.chat.id)
    if on_event is None:
        return
    _I, _err = await FetchMeOnChat(bot, chat_id=event.chat.id)
    if _I == 404:
        print(f"Không thể chỉnh sửa tin nhắn trong {event.chat.id} !\nError: {_err}")
        return
    service_on = await db.get_service_on(int(on_event))
    footer_text = await db.get_footer_text(int(on_event))
    also_footer2photo = await db.get_add_photo_footer(int(on_event))
    is_forward = event.forward_from_chat or event.forward_from
    if (_I.can_edit_messages is True) and (service_on is True) and (footer_text is not None) and (is_forward is None) and (also_footer2photo is True):
        await AddFooter(bot, event, footer_text, int(on_event))


@AHBot.on_message(filters.channel & filters.photo & ~filters.edited & ~filters.private)
async def add_text_footer(bot: Client, event: Message):
    on_event = await db.find_user_id(event.chat.id)
    if on_event is None:
        return
    _I, _err = await FetchMeOnChat(bot, chat_id=event.chat.id)
    if _I == 404:
        print(f"Không thể chỉnh sửa tin nhắn trong {event.chat.id} !\nError: {_err}")
        return
    service_on = await db.get_service_on(int(on_event))
    footer_text = await db.get_footer_text(int(on_event))
    also_footer2text = await db.get_add_text_footer(int(on_event))
    is_forward = event.forward_from_chat or event.forward_from
    if (_I.can_edit_messages is True) and (service_on is True) and (footer_text is not None) and (is_forward is None) and (also_footer2text is True):
        await AddFooter(bot, event, footer_text, int(on_event))


@AHBot.on_message(filters.private & filters.command("broadcast") & filters.user(Config.BOT_OWNER) & filters.reply)
async def _broadcast(_, event: Message):
    await broadcast_handler(event)


@AHBot.on_message(filters.private & filters.command("status") & filters.user(Config.BOT_OWNER))
async def _status(_, event: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await db.total_users_count()
    await event.reply_text(
        text=f"**Tổng dung lượng đĩa:** {total} \n**Không gian được sử dụng:** {used}({disk_usage}%) \n**Không gian còn trống:** {free} \n**Sử dụng CPU:** {cpu_usage}% \n**Sử dụng RAM:** {ram_usage}%\n\n**Tổng số người dùng trong DB:** `{total_users}`",
        parse_mode="Markdown",
        quote=True
    )


@AHBot.on_message(filters.private & filters.command("disable") & filters.user(Config.BOT_OWNER))
async def handler_disabler(bot: Client, event: Message):
    if len(event.command) > 1:
        if event.command[1].startswith("-100"):
            get_user_id = await db.find_user_id(channel_id=int(event.command[1]))
            if get_user_id is None:
                await event.reply_text(f"Trò chuyện không tìm thấy trong cơ sở dữ liệu!")
            else:
                await db.delete_user(user_id=get_user_id)
                await event.reply_text(f"ữ liệu người dùng của {str(get_user_id)} đã xóa khỏi cơ sở dữ liệu!")
                await bot.leave_chat(chat_id=event.chat.id)
        else:
            await db.delete_user(user_id=int(event.command[1]))
            await event.reply_text(f"Dữ liệu người dùng của {event.command[1]} đã xóa khỏi cơ sở dữ liệu!")


@AHBot.on_callback_query()
async def callback_handlers(bot: Client, cb: CallbackQuery):
    if cb.message.chat.type not in ["private"]:
        return
    if "triggerService" in cb.data:
        cache_service_on = await db.get_service_on(cb.from_user.id)
        await db.set_service_on(cb.from_user.id, service_on=(False if (cache_service_on is True) else True))
        await cb.answer("Đã thay đổi chế độ dịch vụ thành công", show_alert=True)
        await ShowSettings(cb.message, user_id=cb.from_user.id)
    elif "setAlsoFooter2Text" in cb.data:
        cache_also_footer2text = await db.get_add_text_footer(cb.from_user.id)
        await db.set_add_text_footer(cb.from_user.id, add_text_footer=(False if (cache_also_footer2text is True) else True))
        await cb.answer(f"Ok, Tôi sẽ {'không ' if (cache_also_footer2text is True) else ''}thêm Chân trang vào Tin nhắn Văn bản nữa!", show_alert=True)
        await ShowSettings(cb.message, user_id=cb.from_user.id)
    elif "setAlsoFooter2Photo" in cb.data:
        cache_also_footer2photo = await db.get_add_photo_footer(cb.from_user.id)
        await db.set_add_photo_footer(cb.from_user.id, add_photo_footer=(False if (cache_also_footer2photo is True) else True))
        await cb.answer(f"Ok, Tôi sẽ {'không ' if (cache_also_footer2photo is True) else ''}thêm Chân trang vào Ảnh!", show_alert=True)
        await ShowSettings(cb.message, user_id=cb.from_user.id)
    elif "setFooterText" in cb.data:
        await cb.message.edit("Bây giờ gửi cho tôi văn bản chân trang. Tối đa 1024 ký tự.\n\nNhập /cancel để Hủy quá trình này.")
        try:
            event_: Message = await bot.listen(cb.message.chat.id, filters=filters.text, timeout=300)
            if event_.text:
                if event_.text == "/cancel":
                    await event_.delete(True)
                    await cb.message.edit("Process Cancelled!")
                else:
                    cache_footer = event_.text.markdown
                    await db.set_footer_text(cb.from_user.id, cache_footer)
                    await cb.message.edit(
                        text=f"Chân trang đã được thêm!\n\n**Văn bản chân trang:**\n{cache_footer}",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Đi tới Cài đặt", callback_data="showSettings")]])
                    )
        except TimeoutError:
            await cb.message.edit("5 phút trôi qua!\nBây giờ kích hoạt lại từ /settings 😐")
    elif "showSettings" in cb.data:
        await ShowSettings(cb.message, user_id=cb.from_user.id)
    elif "rmFooterText" in cb.data:
        await db.set_footer_text(cb.from_user.id, footer_text=None)
        await cb.answer("Footer Text Removed!", show_alert=True)
        await ShowSettings(cb.message, user_id=cb.from_user.id)
    elif "showFooterText" in cb.data:
        footer_text = await db.get_footer_text(cb.from_user.id)
        await cb.message.edit(f"**Văn bản chân trang:**\n{footer_text}", parse_mode="markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Đi tới Cài đặt", callback_data="showSettings")]]))
    elif "setChannelID" in cb.data:
        await cb.message.edit(
            text="Ok ,\nBây giờhêm tôi vào Kênh với tư cách Quản trị viên & Chuyển tiếp Tin nhắn Từ Kênh.\n\nNhấn /cancel để Hủy quá trình này."
        )
        try:
            event_: Message = await bot.listen(cb.message.chat.id, timeout=300)
            if event_.forward_from_chat and ((await db.is_user_exist(event_.forward_from_chat.id)) is False):
                try:
                    _I, _err = await FetchMeOnChat(bot, chat_id=event_.forward_from_chat.id)
                    if _I == 404:
                        await cb.message.edit(f"Không thể chỉnh sửa tin nhắn trong {str(event_.forward_from_chat.id)} !\nError: {_err}")
                        return
                    if _I and (_I.can_edit_messages is True):
                        if await db.find_user_id(channel_id=event_.forward_from_chat.id) is None:
                            try:
                                UserClient = await bot.get_chat_member(chat_id=event_.forward_from_chat.id, user_id=(await bot.get_me()).id)
                                if UserClient.can_edit_messages is True:
                                    await db.set_channel_id(cb.from_user.id, channel_id=event_.forward_from_chat.id)
                                    await cb.message.edit("Đã thêm thành công kênh vào cơ sở dữ liệu!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Đi tới Cài đặt", callback_data="showSettings")]]))
                                else:
                                    await cb.message.edit("Sorry,\nBạn không có quyền Chỉnh sửa Tin nhắn trên Kênh này!")
                            except:
                                await cb.message.edit("Sorry,\nBạn không phải là Quản trị viên của kênh này!")
                        else:
                            await cb.message.edit("Sorry,\nĐã có kênh này trong Cơ sở dữ liệu! Không thể thêm lại cùng một kênh.")
                    else:
                        await cb.message.edit(f"Tôi không có quyền chỉnh sửa tin nhắn trong {_I.title} !!\n\nVui lòng cho phép người khác Tôi không thể thêm Chân trang.")
                except UserNotParticipant:
                    await cb.message.edit("Không thể thêm kênh vào cơ sở dữ liệu!\nTôi không phải là Quản trị viên trong Kênh.")
                except Exception as err:
                    await cb.message.edit(f"Không thể tìm thấy kênh!\n\n**Error:** `{err}`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("OWOHUB 🔞", url="https://t.me/OWOHUB")]]))
            elif event_.text and (event_.text == "/cancel"):
                await cb.message.edit("Quá trình bị hủy!")
        except TimeoutError:
            await cb.message.edit("Unkil,\n5 phút trôi qua!\nBây giờ kích hoạt lại từ /settings 😐")


AHBot.run()
