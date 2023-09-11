from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message
from config import BANNED_USERS, AUTO_DOWNLOADS_CLEAR, STREAM_IMG, STREAM_IMG, STREAM_IMG
from Bgt.platforms import YouTube
from Bgt import app
from Bgt.misc import db
from Bgt.core.call import JavaCall
from Bgt.utils.database import get_loop
from Bgt.utils.thumbnails import gen_thumb
from Bgt.utils.decorators import AdminActual
from Bgt.utils.stream.autoclear import auto_clean
from Bgt.utils.inline.play import stream_markup, telegram_markup, close_keyboard


@app.on_message(filters.command(["skip", "cskip", "vskip"]) & filters.group & ~BANNED_USERS)
@AdminActual
async def skip(cli, message: Message, chat_id):
    if not len(message.command) == 1:
        loop = await get_loop(chat_id)
        if loop != 0:
            return await message.reply_text("ᴜɴᴀʙʟᴇ ᴛᴏ sᴋɪᴘ ᴛᴏ ᴀ sᴘᴇᴄɪꜰɪᴄ ᴛʀᴀᴄᴋ ʙᴇᴄᴀᴜsᴇ ᴏꜰ ᴇɴᴀʙʟᴇᴅ **ʟᴏᴏᴘ ᴘʟᴀʏ**. ᴘʟᴇᴀsᴇ ᴅɪsᴀʙʟᴇ ʟᴏᴏᴘ ᴘʟᴀʏ ᴠɪᴀ `/loop disable` ᴛᴏ ᴜsᴇ ᴛʜɪs ꜰᴇᴀᴛᴜʀᴇ ​.")
        state = message.text.split(None, 1)[1].strip()
        if state.isnumeric():
            state = int(state)
            check = db.get(chat_id)
            if check:
                count = len(check)
                if count > 2:
                    count = int(count - 1)
                    if 1 <= state <= count:
                        for x in range(state):
                            popped = None
                            try:
                                popped = check.pop(0)
                            except:
                                return await message.reply_text("ꜰᴀɪʟᴇᴅ ᴛᴏ sᴋɪᴘ ᴛᴏ sᴘᴇᴄɪꜰɪᴄ ᴛʀᴀᴄᴋ ​.\n\nᴄʜᴇᴄᴋ ʟᴇꜰᴛ ǫᴜᴇᴜᴇ ʙʏ /queue")
                            if popped:
                                if AUTO_DOWNLOADS_CLEAR == str(True):
                                    await auto_clean(popped)
                            if not check:
                                try:
                                    await message.reply_text(
                                        "sᴛʀᴇᴀᴍ sᴋɪᴩᴩᴇᴅ ⏭\n│ \n└ʙʏ : {0} \n\n**» ɴᴏ ᴍᴏʀᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ɪɴ** {1} **ʟᴇᴀᴠɪɴɢ ᴠɪᴅᴇᴏᴄʜᴀᴛ.**".format(message.from_user.mention, message.chat.title),
                                        reply_markup=close_keyboard
                                    )
                                    await JavaCall.stop_stream(chat_id)
                                except:
                                    return
                                break
                    else:
                        return await message.reply_text("ɴᴏᴛ ᴇɴᴏᴜɢʜ ᴛʀᴀᴄᴋs ɪɴ ǫᴜᴇᴜᴇ ꜰᴏʀ ᴛʜᴇ ᴠᴀʟᴜᴇ ɢɪᴠᴇɴ ʙʏ ʏᴏᴜ​. ᴘʟᴇᴀsᴇ ᴄʜᴏᴏsᴇ ɴᴜᴍʙᴇʀs ʙᴇᴛᴡᴇᴇɴ 1 ᴀɴᴅ {0}".format(count))
                else:
                    return await message.reply_text("ᴀᴛʟᴇᴀsᴛ 2 ᴛʀᴀᴄᴋs ɴᴇᴇᴅᴇᴅ ɪɴ ǫᴜᴇᴜᴇ ᴛᴏ sᴋɪᴘ ᴛᴏ ᴀ sᴘᴇᴄɪꜰɪᴄ ɴᴜᴍʙᴇʀ ​. ᴄʜᴇᴄᴋ ǫᴜᴇᴜᴇ ʙʏ /queue")
            else:
                return await message.reply_text("ǫᴜᴇᴜᴇᴅ ʟɪsᴛ ɪs ᴇᴍᴘᴛʏ. ɴᴏ ᴛʀᴀᴄᴋs ғᴏᴜɴᴅ")
        else:
            return await message.reply_text("ᴘʟᴇᴀsᴇ ᴜsᴇ ɴᴜᴍᴇʀɪᴄ ɴᴜᴍʙᴇʀs ꜰᴏʀ sᴘᴇᴄɪꜰɪᴄ ᴛʀᴀᴄᴋs ​, ʟɪᴋᴇ 1, 2 ᴏʀ 3 ᴇᴛᴄ")
    else:
        check = db.get(chat_id)
        popped = None
        try:
            popped = check.pop(0)
            if popped:
                if AUTO_DOWNLOADS_CLEAR == str(True):
                    await auto_clean(popped)
            if not check:
                await message.reply_text(
                    "sᴛʀᴇᴀᴍ sᴋɪᴩᴩᴇᴅ ⏭\n│ \n└ʙʏ : {0} \n\n**» ɴᴏ ᴍᴏʀᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ɪɴ** {1} **ʟᴇᴀᴠɪɴɢ ᴠɪᴅᴇᴏᴄʜᴀᴛ.**".format(message.from_user.mention, message.chat.title),
                    reply_markup=close_keyboard
                )
                try:
                    return await JavaCall.stop_stream(chat_id)
                except:
                    return
        except:
            try:
                await message.reply_text(
                    "sᴛʀᴇᴀᴍ sᴋɪᴩᴩᴇᴅ ⏭\n│ \n└ʙʏ : {0} \n\n**» ɴᴏ ᴍᴏʀᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ɪɴ** {1} **ʟᴇᴀᴠɪɴɢ ᴠɪᴅᴇᴏᴄʜᴀᴛ.**".format(message.from_user.mention, message.chat.title),
                    reply_markup=close_keyboard
                )
                return await JavaCall.stop_stream(chat_id)
            except:
                return

    queued = check[0]["file"]
    title = (check[0]["title"]).title()
    user = check[0]["by"]
    streamtype = check[0]["streamtype"]
    videoid = check[0]["vidid"]
    duration_min = check[0]["dur"]
    status = True if str(streamtype) == "video" else None

    if "live_" in queued:
        n, link = await YouTube.video(videoid, True)
        if n == 0:
            return await message.reply_text("ᴇʀʀᴏʀ ᴡʜɪʟᴇ ᴄʜᴀɴɢɪɴɢ sᴛʀᴇᴀᴍ ᴛᴏ **{0}** ​\n\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴀɢᴀɪɴ.".format(title))
        try:
            await JavaCall.skip_stream(chat_id, link, video=status)
        except:
            return await message.reply_text("**ꜰᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ**\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʀᴀᴄᴋ ᴀɢᴀɪɴ.")

        button = telegram_markup(chat_id)
        img = await gen_thumb(videoid)
        run = await message.reply_photo(
            photo=img,
            caption="⊱ **Tɪᴛʟᴇ :** [{0}]({1})\n⊱ **Dᴜʀᴀᴛɪᴏɴ :** {2} ᴍɪɴᴜᴛᴇs\n⊱ **Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** {3}".format(user, f"https://t.me/{app.username}?start=info_{videoid}"),
            reply_markup=InlineKeyboardMarkup(button),
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "tg"

    elif "vid_" in queued:
        mystic = await message.reply_text("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ɴᴇxᴛ ᴛʀᴀᴄᴋ ꜰʀᴏᴍ ᴘʟᴀʏʟɪsᴛ", disable_web_page_preview=True)
        try:
            file_path, direct = await YouTube.download(videoid, mystic, videoid=True, video=status)
        except:
            return await mystic.edit_text("**ꜰᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ**\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʀᴀᴄᴋ ᴀɢᴀɪɴ.")
        try:
            await JavaCall.skip_stream(chat_id, file_path, video=status)
        except:
            return await mystic.edit_text("**ꜰᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ**\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʀᴀᴄᴋ ᴀɢᴀɪɴ.")
        button = stream_markup(videoid, chat_id)
        img = await gen_thumb(videoid)
        run = await message.reply_photo(
            photo=img,
            caption="⊱ **Tɪᴛʟᴇ :** [{0}]({1})\n⊱ **Dᴜʀᴀᴛɪᴏɴ :** {2} ᴍɪɴᴜᴛᴇs\n⊱ **Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** {3}".format(
                    title[:27],
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    duration_min,
                    user,
                ),
            reply_markup=InlineKeyboardMarkup(button),
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "stream"
        await mystic.delete()

    elif "index_" in queued:
        try:
            await JavaCall.skip_stream(chat_id, videoid, video=status)
        except:
            return await message.reply_text("**ꜰᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ**\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʀᴀᴄᴋ ᴀɢᴀɪɴ.")
        button = telegram_markup(chat_id)
        run = await message.reply_photo(
            photo=STREAM_IMG,
            caption="⊱ **sᴛʀᴇᴀᴍ ᴛʏᴘᴇ :** ʟɪᴠᴇ sᴛʀᴇᴀᴍ [ᴜʀʟ]\n⊱ **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:** {0}".format(user),
            reply_markup=InlineKeyboardMarkup(button),
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "tg"

    else:
        try:
            await JavaCall.skip_stream(chat_id, queued, video=status)
        except:
            return await message.reply_text("**ꜰᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ**\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʀᴀᴄᴋ ᴀɢᴀɪɴ.")
        if videoid == "telegram":
            button = telegram_markup(chat_id)
            run = await message.reply_photo(
                photo=STREAM_IMG
                if str(streamtype) == "audio"
                else STREAM_IMG,
                caption="⊱ **Tɪᴛʟᴇ:** {0}\n⊱ **Dᴜʀᴀᴛɪᴏɴ:** {1}\n⊱ **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:** {2} ".format(title, check[0]["dur"], user),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        else:
            button = stream_markup(videoid, chat_id)
            img = await gen_thumb(videoid)
            run = await message.reply_photo(
                photo=img,
                caption="⊱ **Tɪᴛʟᴇ :** [{0}]({1})\n⊱ **Dᴜʀᴀᴛɪᴏɴ :** {2} ᴍɪɴᴜᴛᴇs\n⊱ **Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** {3}".format(
                    title[:27],
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    duration_min,
                    user,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
