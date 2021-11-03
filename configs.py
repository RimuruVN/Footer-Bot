# (c) @AbirHasan2005

import os


class Config(object):
    API_ID = int(os.environ.get("API_ID", 1234567))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    SESSION_NAME = os.environ.get("SESSION_NAME", "Footer-Bot")
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", -100))
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", None)
    BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", False))
    BOT_OWNER = int(os.environ.get("BOT_OWNER", 2072962525))
    MONGODB_URI = os.environ.get("MONGODB_URI", "")
    START_TEXT = """
Xin chào, tôi là Bot Footer Broadcast!

Tôi có thể thêm chân trang vào Tin nhắn Phương tiện Kênh. Chỉ cần thêm tôi vào kênh với tư cách là Quản trị viên với tất cả các quyền và thiết lập /settings !!
"""
