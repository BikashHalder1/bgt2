from datetime import datetime
from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import Message
from Bgt import app
from Bgt.core.call import JavaCall
from Bgt.utils import bot_sys_stats


__MODULE__ = "Aʟɪᴠᴇ"
__HELP__ = """
⊱ /start - ɢᴇᴛ sᴛᴀʀᴛ ᴍᴇssᴀɢᴇ ᴘᴀɴᴇʟ

⊱ /help - ɢᴇᴛ ʜᴇʟᴘ ᴄᴏᴍᴍᴀɴᴅs ᴍᴇɴᴜ

⊱ /ping - ᴄʜᴇᴄᴋ ᴘɪɴɢ ᴏғ ᴛʜᴇ ʙᴏᴛ
"""


@app.on_message(filters.command(["ping"]) & ~BANNED_USERS)
async def ping_com(client, message: Message):
    try:
        await message.delete()
    except:
        pass
    response = await message.reply_text("» **BGT**")
    start = datetime.now()
    pytgping = await JavaCall.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        "**❕ᴘɪɴɢ ᴛᴀꜱᴋ ᴇxᴇᴄᴜᴛᴇᴅ**\n**   ⊱ ᴛɪᴍᴇ ᴛᴀᴋᴇɴ:** `{0}ᴍs`\n**   ⊱ ᴜᴘᴛɪᴍᴇ:** `{1}`\n\n**❕sʏsᴛᴇᴍ sᴛᴀᴛs**\n**   ⊱ ᴄᴘᴜ:** `{4}`\n**   ⊱ ᴅɪsᴋ:** `{2}`\n**   ⊱ ʀᴀᴍ:** `{3}`\n**   ⊱ ᴩʏ-ᴛɢᴄᴀʟʟs :** `{5}ᴍs`".format(resp, UP, DISK, RAM, CPU, pytgping)
    )
