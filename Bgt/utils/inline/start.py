from config import SUPPORT_HEHE
from Bgt import app
from pyrogram.types import InlineKeyboardButton


def start_pannel():
    buttons = [
            [
                InlineKeyboardButton(text="➕ Aᴅᴅ Mᴇ ➕", url=f"https://t.me/{app.username}?startgroup=new")
            ],
            [
                InlineKeyboardButton(text="Hᴇʟᴘ Mᴇɴᴜ", url=f"https://t.me/{app.username}?start=help")
            ],
            [
                InlineKeyboardButton(text="Sᴇᴛᴛɪɴɢ", callback_data="settings_helper")
            ]
        ]
    return buttons


def private_panel():
    buttons = [
        [
            InlineKeyboardButton(
                text="➕ Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ➕",
                url=f"https://t.me/{app.username}?startgroup=new",
            )
        ],
        [
            InlineKeyboardButton(text="Uᴘᴅᴀᴛᴇꜱ", url="https://t.me/BikashGadgetsTech"),
            InlineKeyboardButton(text="Sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_HEHE}")
        ],
        [
            InlineKeyboardButton(text="ʏᴏᴜᴛᴜʙᴇ", url="https://youtube.com/@BikashGadgetsTech")
        ],
        [
            InlineKeyboardButton(text="Hᴇʟᴘ Mᴇɴᴜ", callback_data="home_help"),
        ]
    ]
    return buttons
