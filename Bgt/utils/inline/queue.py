from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def queue_markup(CPLAY, videoid):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="📑 Qᴜᴇᴜᴇᴅ", callback_data=f"GetQueued {CPLAY}|{videoid}"),
                InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
            ]
    ]
    )
    return upl


def queue_back_markup(CPLAY):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data=f"queue_back_timer {CPLAY}"),
                InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
            ]
        ]
    )
    return upl
