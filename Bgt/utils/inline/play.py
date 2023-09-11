from config import SUPPORT_GROUP
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def stream_markup(videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="sᴘᴇᴇᴅ", callback_data=f"PanelMarkup {videoid}|{chat_id}"),
            InlineKeyboardButton(text="ᴘʟᴀʏʟɪsᴛ", callback_data=f"add_playlist {videoid}")
        ],
        [
            InlineKeyboardButton(text="ʏᴏᴜᴛᴜʙᴇ", url="https://youtube.com/@BikashGadgetsTech")
        ],
        [
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
        ]
    ]
    return buttons


def telegram_markup(chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="ʏᴏᴜᴛᴜʙᴇ", url="https://youtube.com/@BikashGadgetsTech")
        ],
        [
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
        ],
    ]
    return buttons


def track_markup(videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(text="🎧 ᴀᴜᴅɪᴏ", callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"),
            InlineKeyboardButton(text="🎥 ᴠɪᴅᴇᴏ", callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}")
        ],
        [
            InlineKeyboardButton(text="ʏᴏᴜᴛᴜʙᴇ", url="https://youtube.com/@BikashGadgetsTech")
        ],
        [
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data=f"forceclose {videoid}|{user_id}")
        ]
    ]
    return buttons


def livestream_markup(videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(text="ʟɪᴠᴇ sᴛʀᴇᴀᴍ", callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}")
        ],
        [
            InlineKeyboardButton(text="ʏᴏᴜᴛᴜʙᴇ", url="https://youtube.com/@BikashGadgetsTech")
        ],
        [
            InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", url=f"{SUPPORT_GROUP}"),
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data=f"forceclose {videoid}|{user_id}")
        ]
    ]
    return buttons


def playlist_markup(videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(text="🎧 ᴀᴜᴅɪᴏ", callback_data=f"JavaPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}"),
            InlineKeyboardButton(text="🎥 ᴠɪᴅᴇᴏ", callback_data=f"JavaPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}")
        ],
        [
            InlineKeyboardButton(text="ʏᴏᴜᴛᴜʙᴇ", url="https://youtube.com/@BikashGadgetsTech")
        ],
        [
            InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", url=f"{SUPPORT_GROUP}"),
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data=f"forceclose {videoid}|{user_id}")
        ]
    ]
    return buttons


def slider_markup(videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(text="🎧 ᴀᴜᴅɪᴏ", callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"),
            InlineKeyboardButton(text="🎥 ᴠɪᴅᴇᴏ", callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}")
        ],
        [
            InlineKeyboardButton(text="◁", callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}"),
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data=f"forceclose {query}|{user_id}"),
            InlineKeyboardButton(text="▷", callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}")
        ]
    ]
    return buttons


close_keyboard = InlineKeyboardMarkup( 
            [
                [
                    InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
                ]    
            ]
        )


def panel_markup_3(videoid, chat_id):
    buttons = [
            [
                InlineKeyboardButton(text="0.5x", callback_data=f"SpeedUP {chat_id}|0.5"),
                InlineKeyboardButton(text="0.75x", callback_data=f"SpeedUP {chat_id}|0.75"),
                InlineKeyboardButton(text="1.5x", callback_data=f"SpeedUP {chat_id}|1.5")
                
            ],
            [
                InlineKeyboardButton(text="ɴᴏʀᴍᴀʟ", callback_data=f"SpeedUP {chat_id}|1.0"),
                InlineKeyboardButton(text="2.0x", callback_data=f"SpeedUP {chat_id}|2.0"),
                InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data=f"MainMarkup {videoid}|{chat_id}")
            ], 
    ]
    return buttons
                    
