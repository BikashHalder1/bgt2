from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import Message
from Bgt import app
from Bgt.core.call import JavaCall
from Bgt.utils.database import set_loop
from Bgt.utils.inline.play import close_keyboard
from Bgt.utils.decorators import AdminActual


@app.on_message(filters.command(["stop", "end", "cstop", "cend"]) & filters.group & ~BANNED_USERS)
@AdminActual
async def stop_music(cli, message: Message, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text("ᴇʀʀᴏʀ ! ᴡʀᴏɴɢ ᴜsᴀɢᴇ ᴏғ ᴄᴏᴍᴍᴀɴᴅ")
    await JavaCall.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(
        "**sᴛʀᴇᴀᴍ ᴇɴᴅᴇᴅ** \n│ \n└ʙʏ : {} ".format(message.from_user.mention),
        reply_markup=close_keyboard,
    )
