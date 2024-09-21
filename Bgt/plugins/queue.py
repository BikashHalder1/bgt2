import asyncio
from config import BANNED_USERS, STREAM_IMG
from pyrogram import filters
from pyrogram.types import CallbackQuery, InputMediaPhoto, Message
from Bgt.platforms import YouTubeAPI
from Bgt import app
from Bgt.misc import db
from Bgt.utils.thumbnails import gen_thumb
from Bgt.utils import Javabin, get_channeplayCB
from Bgt.utils.formatters import seconds_to_min
from Bgt.utils.database import get_cmode, is_active_chat
from Bgt.utils.inline import queue_back_markup, queue_markup


basic = {}


def get_duration(playing):
    file_path = playing[0]["file"]
    if "index_" in file_path or "live_" in file_path:
        return "ᴜɴᴋɴᴏᴡɴ"
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return "ᴜɴᴋɴᴏᴡɴ"
    else:
        return seconds_to_min(duration_seconds)


@app.on_message(filters.command(["queue", "cqueue", "player", "cplayer"]) & filters.group & ~BANNED_USERS)
async def queue_com(client, message: Message):
    try:
        await message.delete()
    except:
        pass
    if message.command[0][0] == "c":
        chat_id = await get_cmode(message.chat.id)
        if chat_id is None:
            return await message.reply_text("ᴄᴀɴ'ᴛ ᴄʜᴀɴɢᴇ ᴘʟᴀʏ ᴍᴏᴅᴇ ɪɴ ᴀᴄᴛɪᴠᴇ ɢʀᴏᴜᴘ ᴄᴀʟʟ. ᴘʟᴇᴀsᴇ sᴛᴏᴘ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ꜰɪʀsᴛ ᴡɪᴛʜ /stop or /end.")
        try:
            await app.get_chat(chat_id)
        except:
            return await message.reply_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ᴄʜᴀɴɴᴇʟ.\n\nᴍᴀᴋᴇ sᴜʀᴇ ʏᴏᴜ ʜᴀᴠᴇ ᴀᴅᴅᴇᴅ ʙᴏᴛ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴘʀᴏᴍᴏᴛᴇᴅ ɪᴛ ᴀs ᴀᴅᴍɪɴ.\nᴇᴅɪᴛ ᴏʀ ᴄʜᴀɴɢᴇ ᴄʜᴀɴɴᴇʟ ᴠɪᴀ /channelplay")
        cplay = True
    else:
        chat_id = message.chat.id
        cplay = False
    if not await is_active_chat(chat_id):
        return await message.reply_text("ʙᴏᴛ ɪsɴ'ᴛ sᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ")
    got = db.get(chat_id)
    if not got:
        return await message.reply_text("ǫᴜᴇᴜᴇᴅ ʟɪsᴛ ɪs ᴇᴍᴘᴛʏ. ɴᴏ ᴛʀᴀᴄᴋs ғᴏᴜɴᴅ")
    file = got[0]["file"]
    videoid = got[0]["vidid"]
    user = got[0]["by"]
    title = (got[0]["title"]).title()
    typo = (got[0]["streamtype"]).title()
    DUR = get_duration(got)

    if ("live_" in file) or ("vid_" in file):
        IMAGE = await gen_thumb(videoid)
    elif "index_" in file:
        IMAGE = STREAM_IMG
    else:
        if videoid == "telegram":
            IMAGE = STREAM_IMG if typo == "Audio" else STREAM_IMG
        else:
            IMAGE = await gen_thumb(videoid)

    cap = f"""**{app.mention} ᴩʟᴀʏᴇʀ**

⊱ **Tɪᴛʟᴇ:** {title[:27]}
⊱ **Dᴜʀᴀᴛɪᴏɴ:** {DUR}
⊱ **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:** {user}

ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ᴡʜᴏʟᴇ ǫᴜᴇᴜᴇᴅ ʟɪsᴛ."""
    upl = queue_markup("c" if cplay else "g", videoid)
    basic[videoid] = True
    await message.reply_photo(photo=IMAGE, caption=cap, reply_markup=upl)


@app.on_callback_query(filters.regex("GetTimer") & ~BANNED_USERS)
async def quite_timer(client, CallbackQuery: CallbackQuery):
    try:
        await CallbackQuery.answer()
    except:
        pass


@app.on_callback_query(filters.regex("GetQueued") & ~BANNED_USERS)
async def queued_tracks(client, CallbackQuery: CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    what, videoid = callback_request.split("|")
    try:
        chat_id, channel = await get_channeplayCB(what, CallbackQuery)
    except:
        return
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer("ʙᴏᴛ ɪsɴ'ᴛ sᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ", show_alert=True)
    got = db.get(chat_id)
    if not got:
        return await CallbackQuery.answer("ǫᴜᴇᴜᴇᴅ ʟɪsᴛ ɪs ᴇᴍᴘᴛʏ ɴᴏ ᴛʀᴀᴄᴋs ғᴏᴜɴᴅ", show_alert=True)
    if len(got) == 1:
        return await CallbackQuery.answer("ᴏɴʟʏ ᴏɴᴇ ᴛʀᴀᴄᴋ ɪs ɪɴ ǫᴜᴇᴜᴇ ᴀᴅᴅ sᴏᴍᴇ ᴍᴏʀᴇ ᴛʀᴀᴄᴋs ɪɴ ǫᴜᴇᴜᴇ ᴛᴏ ᴄʜᴇᴄᴋ ᴡʜᴏʟᴇ ǫᴜᴇᴜᴇ", show_alert=True)
    await CallbackQuery.answer()
    basic[videoid] = False
    buttons = queue_back_markup(what)
    thumbnail = await YouTube.thumbnail(videoid, True)
    med = InputMediaPhoto(media=thumbnail, caption="» ᴩʟᴇᴀsᴇ ᴡᴀɪᴛ ")
    await CallbackQuery.edit_message_media(media=med)
    j = 0
    msg = ""
    for x in got:
        j += 1
        if j == 1:
            msg += "{0} Pʟᴀʏᴇʀ :\n\n⊱ Tɪᴛʟᴇ : {1}\n⊱ Dᴜʀᴀᴛɪᴏɴ : {2}\n⊱ Bʏ : {3}\n\n".format(app.mention, x["title"], x["dur"], x["by"])
        elif j == 2:
            msg += "Qᴜᴇᴜᴇᴅ :\n\n⊱ Tɪᴛʟᴇ : {0}\n⊱ Dᴜʀᴀᴛɪᴏɴ : {1}\n⊱ Bʏ : {2}\n\n".format(x["title"], x["dur"], x["by"])
        else:
            msg += "⊱ Tɪᴛʟᴇ : {0}\n⊱ Dᴜʀᴀᴛɪᴏɴ : {1}\n⊱ Rᴇǫᴜᴇsᴛᴇᴅ Bʏ : {2}\n\n".format(x["title"], x["dur"], x["by"])

    if "Queued" in msg:
        if len(msg) < 700:
            await asyncio.sleep(1)
            return await CallbackQuery.edit_message_text(msg, reply_markup=buttons)
        if "⊱" in msg:
            msg = msg.replace("⊱", "")
        link = await Javabin(msg)
        if not link:
            return await CallbackQuery.message.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ǫᴜᴇᴜᴇ ʟɪsᴛ")
        med = InputMediaPhoto(media=link, caption="<u>**ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs:</u>**  [ᴄʜᴇᴄᴋᴏᴜᴛ ᴍᴏʀᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ғʀᴏᴍ ʜᴇʀᴇ]({0})".format(link))
        await CallbackQuery.edit_message_media(media=med, reply_markup=buttons)
    else:
        await asyncio.sleep(1)
        return await CallbackQuery.edit_message_text(msg, reply_markup=buttons)


@app.on_callback_query(filters.regex("queue_back_timer") & ~BANNED_USERS)
async def queue_back(client, CallbackQuery: CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cplay = callback_data.split(None, 1)[1]
    try:
        chat_id, channel = await get_channeplayCB(cplay, CallbackQuery)
    except:
        return
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer("ʙᴏᴛ ɪsɴ'ᴛ sᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ", show_alert=True)
    got = db.get(chat_id)
    if not got:
        return await CallbackQuery.answer("ǫᴜᴇᴜᴇᴅ ʟɪsᴛ ɪs ᴇᴍᴘᴛʏ. ɴᴏ ᴛʀᴀᴄᴋs ғᴏᴜɴᴅ", show_alert=True)
    await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ʙᴀᴄᴋ ", show_alert=True)

    file = got[0]["file"]
    videoid = got[0]["vidid"]
    user = got[0]["by"]
    title = (got[0]["title"]).title()
    typo = (got[0]["streamtype"]).title()
    DUR = get_duration(got)
    if ("live_" in file) or ("vid_" in file):
        IMAGE = await gen_thumb(videoid)
    elif "index_" in file:
        IMAGE = STREAM_IMG
    else:
        if videoid == "telegram":
            IMAGE = STREAM_IMG if typo == "Audio" else STREAM_IMG
        else:
            IMAGE = await gen_thumb(videoid)

    cap = f"""**{app.mention} ᴩʟᴀʏᴇʀ**

⊱ **Tɪᴛʟᴇ:** {title[:27]}
⊱ **Dᴜʀᴀᴛɪᴏɴ:** {DUR}
⊱ **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:** {user}

ᴄʟɪᴄᴋ ᴏɴ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ᴡʜᴏʟᴇ ǫᴜᴇᴜᴇᴅ ʟɪsᴛ."""
    upl = queue_markup(cplay, videoid)
    basic[videoid] = True
    med = InputMediaPhoto(media=IMAGE, caption=cap)
    await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
