from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Bgt import app

def help_back_markup():
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data=f"settings_back_helper")
            ]
        ]
    )
    return upl


def private_help_panel():
    buttons = [
        [
            InlineKeyboardButton(text="Hᴇʟᴘ Mᴇɴᴜ", url=f"https://t.me/{app.username}?start=help")
        ]
    ]
    return buttons


def served_panel():
    buttons = [
        [
            InlineKeyboardButton(text="Verify Yourself", url=f"https://t.me/{app.username}?start")
        ]
    ]
    return buttons


# IMAGE
def image_markup(user_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="🏞 Change Image",
                callback_data=f"change_images",
            ),
        ],
        [
          InlineKeyboardButton(
              text="🗑 Close",
              callback_data=f"close",
          ),
        ],
    ]
    return buttons

