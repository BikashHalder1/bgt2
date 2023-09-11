from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def botplaylist_markup():
    buttons = [
        [
            InlineKeyboardButton(text="ᴘʟᴀʏ ᴘʟᴀʏʟɪsᴛ", callback_data="get_playlist_playmode")
        ],
        [
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
        ]
    ]
    return buttons


def get_playlist_markup():
    buttons = [
        [
            InlineKeyboardButton(text="🎧 ᴀᴜᴅɪᴏ", callback_data="play_playlist a"),
            InlineKeyboardButton(text="🎥 ᴠɪᴅᴇᴏ", callback_data="play_playlist v")
        ],
        [
            InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="home_play"),
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
        ]
    ]
    return buttons


def warning_markup():
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="❗️ ʏᴇᴀʜ, ᴅᴇʟᴇᴛᴇ ɪᴛ", callback_data="delete_whole_playlist")
            ],
            [
                InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="del_back_playlist"),
                InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
            ]
        ]
    )
    return upl
