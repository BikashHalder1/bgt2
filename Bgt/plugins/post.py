from config import BANNED_USERS, START_IMG
from Bgt import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def post_panel():
    buttons = [
        [
            InlineKeyboardButton(
                text="➕ Aᴅᴅ Mᴇ ➕",
                url=f"https://t.me/{app.username}?startgroup=new",
            )
        ],
        [
            InlineKeyboardButton(
                text="📱 ʏᴏᴜᴛᴜʙᴇ 📱",
                url=f"https://youtube.com/@BikashGadgetsTech",
            )
        ]
    ]
    return buttons


@app.on_message(filters.command(["p", "post"]) & (filters.channel | filters.group) & ~BANNED_USERS)
async def help_cmd(_, m):
    try:
        await m.delete()
    except:
        pass
    key = post_panel()
    await m.reply_photo(
        photo=START_IMG,
        caption=f"""
ᴍᴏsᴛ ᴀᴅᴠᴀɴᴄᴇᴅ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴀɴᴅ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘ ᴀɴᴅ ᴄʜᴀɴɴᴇʟ ᴠɪᴅᴇᴏᴄʜᴀᴛs ᴘᴏᴡᴇʀᴇᴅ ʙʏ ʙɢᴛ ✨

‣ 𝟸𝟺x𝟽 ᴜᴘᴛɪᴍᴇ 
‣ ᴍᴜsɪᴄ ʙᴏᴛ ғᴇᴀᴛᴜʀᴇs
‣ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ғᴇᴀᴛᴜʀᴇs
‣ ɪᴛ's sᴇᴄᴜʀᴇ ᴀɴᴅ sᴀғᴇ

ᴀᴅᴅ ᴍᴇ » **{app.mention}**""",
        reply_markup=InlineKeyboardMarkup(key)
    )
