from config import SUPPORT_GROUP
from pyrogram.types import InlineKeyboardButton


def song_markup(vidid):
    buttons = [
        [
            InlineKeyboardButton(
                text="🔊 ᴀᴜᴅɪᴏ",
                callback_data=f"song_helper audio|{vidid}",
            ),
            InlineKeyboardButton(
                text="🎥 ᴠɪᴅᴇᴏ",
                callback_data=f"song_helper video|{vidid}",
            ),
        ],
        [
            InlineKeyboardButton(text="sᴜᴩᴩᴏʀᴛ", url=f"{SUPPORT_GROUP}"),
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
        ]
    ]
    return buttons
