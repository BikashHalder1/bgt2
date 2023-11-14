from Bgt import app
from pyrogram.types import InlineKeyboardButton


def verify_pannel():
    buttons = [
            [
                InlineKeyboardButton(text="➕ Verify", url=f"https://t.me/{app.username}?start=verify")
            ]
        ]
    return buttons
