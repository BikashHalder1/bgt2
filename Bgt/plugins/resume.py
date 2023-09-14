from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import Message
from Bgt import app
from Bgt.core.call import JavaCall
from Bgt.utils.inline.play import close_keyboard
from Bgt.utils.decorators import AdminRightsCheck
from Bgt.utils.database import is_music_playing, music_on


@app.on_message(filters.command(["resume", "cresume"]) & filters.group & ~BANNED_USERS & ~filters.forwarded)
@AdminRightsCheck
async def resume_com(cli, message: Message, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text("ᴇʀʀᴏʀ ! ᴡʀᴏɴɢ ᴜsᴀɢᴇ ᴏғ ᴄᴏᴍᴍᴀɴᴅ")
    if await is_music_playing(chat_id):
        return await message.reply_text("ᴍᴜsɪᴄ ɪs ᴀʟʀᴇᴀᴅʏ ʀᴇsᴜᴍᴇᴅ​")
    await music_on(chat_id)
    await JavaCall.resume_stream(chat_id)
    await message.reply_text("**sᴛʀᴇᴀᴍ ʀᴇsᴜᴍᴇᴅ** ʙʏ : {} ".format(message.from_user.mention), reply_markup=close_keyboard)
