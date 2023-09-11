from typing import Union
from pyrogram.types import InlineKeyboardButton


def setting_markup():
    buttons = [
        [
            InlineKeyboardButton(text="🔊 ᴀᴜᴅ ǫᴜᴀʟɪᴛʏ", callback_data="AQ"),
            InlineKeyboardButton(text="🎥 ᴠɪᴅ ǫᴜᴀʟɪᴛʏ", callback_data="VQ")
        ],
        [
            InlineKeyboardButton(text="▶️ ᴘʟᴀʏ ᴍᴏᴅᴇ", callback_data="PM"),
            InlineKeyboardButton(text="🔄 ᴄʟᴇᴀɴ ᴍᴏᴅᴇ", callback_data="CM")
        ],
        [
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
        ]
    ]
    return buttons


def audio_quality_markup(
    low: Union[bool, str] = None,
    medium: Union[bool, str] = None,
    high: Union[bool, str] = None,
):
    buttons = [
        [
            InlineKeyboardButton(
                text="{0} ʟᴏᴡ".format("➻") if low == True else "{0} ʟᴏᴡ".format(""),
                callback_data="LQA",
            )
        ],
        [
            InlineKeyboardButton(
                text="{0} ᴍᴇᴅɪᴜᴍ".format("➻")
                if medium == True
                else "{0} ᴍᴇᴅɪᴜᴍ".format(""),
                callback_data="MQA",
            )
        ],
        [
            InlineKeyboardButton(
                text="{0} ʜɪɢʜ".format("➻")
                if high == True
                else "{0} ʜɪɢʜ".format(""),
                callback_data="HQA",
            )
        ],
        [
            InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="setting_back_help"),
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
        ]
    ]
    return buttons

def video_quality_markup(
    low: Union[bool, str] = None,
    medium: Union[bool, str] = None,
    high: Union[bool, str] = None,
):
    buttons = [
        [
            InlineKeyboardButton(
                text="{0} ʟᴏᴡ".format("➻")
                if low == True
                else "{0} ʟᴏᴡ".format(""),
                callback_data="LQV",
            )
        ],
        [
            InlineKeyboardButton(
                text="{0} ᴍᴇᴅɪᴜᴍ".format("➻")
                if medium == True
                else "{0} ᴍᴇᴅɪᴜᴍ".format(""),
                callback_data="MQV",
            )
        ],
        [
            InlineKeyboardButton(
                text="{0} ʜɪɢʜ".format("➻")
                if high == True
                else "{0} ʜɪɢʜ".format(""),
                callback_data="HQV",
            )
        ],
        [
            InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="setting_back_help"),
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
        ]
    ]
    return buttons


def playmode_users_markup(
    Direct: Union[bool, str] = None,
    Group: Union[bool, str] = None,
    Playtype: Union[bool, str] = None,
):
    buttons = [
        [
            InlineKeyboardButton(text="🔎 sᴇᴀʀᴄʜ ᴍᴏᴅᴇ", callback_data="SEARCHANSWER"),
            InlineKeyboardButton(
                text="✅ ᴅɪʀᴇᴄᴛ" if Direct == True else "✅ ɪɴʟɪɴᴇ",
                callback_data="MODECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(text="▶️ ᴘʟᴀʏ ᴍᴏᴅᴇ", callback_data="AUTHANSWER"),
            InlineKeyboardButton(
                text="👤 ᴀᴅᴍɪɴs" if Group == True else "👥 ᴇᴠᴇʀʏᴏɴᴇ",
                callback_data="CHANNELMODECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(text="🫂 ᴘʟᴀʏ ᴛʏᴘᴇ", callback_data="PLAYTYPEANSWER"),
            InlineKeyboardButton(
                text="👤 ᴀᴅᴍɪɴs" if Playtype == True else "👥 ᴇᴠᴇʀʏᴏɴᴇ",
                callback_data="PLAYTYPECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="setting_back_help"),
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
        ]
    ]
    return buttons


def cleanmode_settings_markup(
    status: Union[bool, str] = None,
    dels: Union[bool, str] = None
):
    buttons = [
        [
            InlineKeyboardButton(
                text="🔄 ᴄʟᴇᴀɴ ᴍᴏᴅᴇ", callback_data="CMANSWER"
            ),
            InlineKeyboardButton(
                text="✅ ᴇɴᴀʙʟᴇᴅ" if status == True else "❌ ᴅɪꜱᴀʙʟᴇᴅ",
                callback_data="CLEANMODE",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🗑 ᴄᴏᴍᴍᴀɴᴅ ᴄʟᴇᴀɴ", callback_data="COMMANDANSWER"
            ),
            InlineKeyboardButton(
                text="✅ ᴇɴᴀʙʟᴇᴅ" if dels == True else "❌ ᴅɪꜱᴀʙʟᴇᴅ",
                callback_data="COMMANDELMODE",
            ),
        ],
        [
            InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="setting_back_help"),
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
        ]
    ]
    return buttons
