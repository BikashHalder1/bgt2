from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import Message
from Bgt.platforms import YouTube
from Bgt import app
from Bgt.misc import db
from Bgt.core.call import JavaCall
from Bgt.utils import AdminActual, seconds_to_min


@app.on_message(filters.command(["seek", "cseek", "seekback", "cseekback"]) & filters.group & ~BANNED_USERS)
@AdminActual
async def seek_comm(_, message: Message, chat_id):
    if len(message.command) == 1:
        return await message.reply_text("**ᴜsᴀɢᴇ:**\n/seek ᴏʀ /seekback [Dᴜʀᴀᴛɪᴏɴ ɪɴ sᴇᴄᴏɴᴅs]")
    query = message.text.split(None, 1)[1].strip()
    if not query.isnumeric():
        return await message.reply_text("ᴩʟᴇᴀsᴇ ᴜsᴇ ɴᴜᴍʙᴇʀ ғᴏʀ sᴇᴇᴋɪɴɢ ɪɴ sᴇᴄᴏɴᴅs.")
    playing = db.get(chat_id)
    if not playing:
        return await message.reply_text("ǫᴜᴇᴜᴇᴅ ʟɪsᴛ ɪs ᴇᴍᴘᴛʏ. ɴᴏ ᴛʀᴀᴄᴋs ғᴏᴜɴᴅ")
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await message.reply_text("sᴏʀʀʏ ʙᴜᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ sᴇᴇᴋ ᴛʜᴇ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ, ɪᴛ ᴄᴀɴ ᴏɴʟʏ ʙᴇ sᴋɪᴩᴩᴇᴅ ᴏʀ sᴛᴏᴩᴩᴇᴅ.")
    file_path = playing[0]["file"]
    if "index_" in file_path or "live_" in file_path:
        return await message.reply_text("sᴏʀʀʏ ʙᴜᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ sᴇᴇᴋ ᴛʜᴇ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ, ɪᴛ ᴄᴀɴ ᴏɴʟʏ ʙᴇ sᴋɪᴩᴩᴇᴅ ᴏʀ sᴛᴏᴩᴩᴇᴅ.")
    duration_played = int(playing[0]["played"])
    duration_to_skip = int(query)
    duration = playing[0]["dur"]
    if message.command[0][-2] == "c":
        if (duration_played - duration_to_skip) <= 10:
            return await message.reply_text(
                "ʙᴏᴛ ɪs ɴᴏᴛ ᴀʙʟᴇ ᴛᴏ sᴇᴇᴋ ʙᴇᴄᴀᴜsᴇ ᴏғ ʜɪɢʜ Dᴜʀᴀᴛɪᴏɴ ɢɪᴠᴇɴ. ᴛʀʏ sᴇᴇᴋɪɴɢ ᴡɪᴛʜ ʟᴏᴡᴇʀ Dᴜʀᴀᴛɪᴏɴ ᴀɴᴅ ʀᴇᴍᴇᴍʙᴇʀ ᴛʜᴀᴛ ᴀ ᴛɪᴍᴇ ᴏғ 10sᴇᴄ ɪs ʟᴇғᴛ ᴀғᴛᴇʀ sᴇᴇᴋɪɴɢ.\n\nᴩʟᴀʏɪɴɢ** {0}** ᴍɪɴs ᴏᴜᴛ ᴏғ **{1}** ᴍɪɴs".format(seconds_to_min(duration_played), duration)
            )
        to_seek = duration_played - duration_to_skip + 1
    else:
        if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
            return await message.reply_text(
                "ʙᴏᴛ ɪs ɴᴏᴛ ᴀʙʟᴇ ᴛᴏ sᴇᴇᴋ ʙᴇᴄᴀᴜsᴇ ᴏғ ʜɪɢʜ Dᴜʀᴀᴛɪᴏɴ ɢɪᴠᴇɴ. ᴛʀʏ sᴇᴇᴋɪɴɢ ᴡɪᴛʜ ʟᴏᴡᴇʀ Dᴜʀᴀᴛɪᴏɴ ᴀɴᴅ ʀᴇᴍᴇᴍʙᴇʀ ᴛʜᴀᴛ ᴀ ᴛɪᴍᴇ ᴏғ 10sᴇᴄ ɪs ʟᴇғᴛ ᴀғᴛᴇʀ sᴇᴇᴋɪɴɢ.\n\nᴩʟᴀʏɪɴɢ** {0}** ᴍɪɴs ᴏᴜᴛ ᴏғ **{1}** ᴍɪɴs".format(seconds_to_min(duration_played), duration)
            )
        to_seek = duration_played + duration_to_skip + 1
    mystic = await message.reply_text("sᴇᴇᴋɪɴɢ")
    if "vid_" in file_path:
        n, file_path = await YouTube.video(playing[0]["vidid"], True)
        if n == 0:
            return await message.reply_text("sᴏʀʀʏ ʙᴜᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ sᴇᴇᴋ ᴛʜᴇ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ, ɪᴛ ᴄᴀɴ ᴏɴʟʏ ʙᴇ sᴋɪᴩᴩᴇᴅ ᴏʀ sᴛᴏᴩᴩᴇᴅ.")
    try:
        await JavaCall.seek_stream(
            chat_id,
            file_path,
            seconds_to_min(to_seek),
            duration,
            playing[0]["streamtype"],
        )
    except:
        return await mystic.edit_text("ғᴀɪʟᴇᴅ ᴛᴏ sᴇᴇᴋ")
    if message.command[0][-2] == "c":
        db[chat_id][0]["played"] -= duration_to_skip
    else:
        db[chat_id][0]["played"] += duration_to_skip
    await mystic.edit_text("sᴇᴇᴋᴇᴅ ᴛᴏ {0} ᴍɪɴs".format(seconds_to_min(to_seek)))
