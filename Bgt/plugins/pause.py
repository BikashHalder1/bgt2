from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import Message
from Bgt import app
from Bgt.core.call import JavaCall
from Bgt.utils.inline.play import close_keyboard
from Bgt.utils.decorators import AdminRightsCheck
from Bgt.utils.database import is_music_playing, music_off


@app.on_message(filters.command(["pause", "cpause"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def pause_admin(cli, message: Message, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text("ᴇʀʀᴏʀ ! ᴡʀᴏɴɢ ᴜsᴀɢᴇ ᴏғ ᴄᴏᴍᴍᴀɴᴅ")
    if not await is_music_playing(chat_id):
        return await message.reply_text("ᴍᴜsɪᴄ ɪs ᴀʟʀᴇᴀᴅʏ ᴘᴀᴜsᴇᴅ​")
    await music_off(chat_id)
    await JavaCall.pause_stream(chat_id)
    await message.reply_text(
        "**sᴛʀᴇᴀᴍ ᴩᴀᴜsᴇᴅ** ʙʏ : {}".format(message.from_user.mention),
        reply_markup=close_keyboard
    )
