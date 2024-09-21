import random
from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup
from config import AUTO_DOWNLOADS_CLEAR, BANNED_USERS, STREAM_IMG
from Bgt.platforms import YouTubeAPI
from Bgt import app
from Bgt.core.call import JavaCall
from Bgt.misc import db
from Bgt.utils.database import is_active_chat, is_music_playing, music_off, music_on, set_loop
from Bgt.utils import seconds_to_min, ActualAdminCB
from Bgt.utils.inline import stream_markup, panel_markup_3, telegram_markup
from Bgt.utils.inline.play import close_keyboard
from Bgt.utils.stream.autoclear import auto_clean
from Bgt.utils.thumbnails import gen_thumb


checker = {}


@app.on_callback_query(filters.regex("PanelMarkup") & ~BANNED_USERS)
async def markup_panel(client, CallbackQuery: CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, chat = callback_request.split("|")
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer("ʙᴏᴛ ɪsɴ'ᴛ sᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ", show_alert=True)
    buttons = panel_markup_3(videoid, chat_id)
    try:
        await CallbackQuery.edit_message_reply_markup(InlineKeyboardMarkup(buttons))
    except:
        return


@app.on_callback_query(filters.regex("MainMarkup") & ~BANNED_USERS)
async def del_back_playlist(client, CallbackQuery: CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, chat_id = callback_request.split("|")
    if videoid == str(None):
        buttons = telegram_markup(chat_id)
    else:
        buttons = stream_markup(videoid, chat_id)
    chat_id = CallbackQuery.message.chat.id
    try:
        await CallbackQuery.edit_message_reply_markup(InlineKeyboardMarkup(buttons))
    except:
        return
    if chat_id not in checker:
        checker[chat_id] = {}
    checker[chat_id][CallbackQuery.message.id] = True



@app.on_callback_query(filters.regex("ADMIN") & ~BANNED_USERS)
@ActualAdminCB
async def del_back_playlist(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    command, chat = callback_request.split("|")
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer("ʙᴏᴛ ɪsɴ'ᴛ sᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ", show_alert=True)

    mention = CallbackQuery.from_user.mention

    if command == "Pause":
        if not await is_music_playing(chat_id):
            return await CallbackQuery.answer("ᴍᴜsɪᴄ ɪs ᴀʟʀᴇᴀᴅʏ ᴘᴀᴜsᴇᴅ​", show_alert=True)
        await CallbackQuery.answer()
        await music_off(chat_id)
        await JavaCall.pause_stream(chat_id)
        await CallbackQuery.message.reply_text("⊱ **sᴛʀᴇᴀᴍ ᴩᴀᴜsᴇᴅ** ʙʏ : {} ".format(mention), reply_markup=close_keyboard)

    elif command == "Resume":
        if await is_music_playing(chat_id):
            return await CallbackQuery.answer("ᴍᴜsɪᴄ ɪs ᴀʟʀᴇᴀᴅʏ ʀᴇsᴜᴍᴇᴅ​", show_alert=True)
        await CallbackQuery.answer()
        await music_on(chat_id)
        await JavaCall.resume_stream(chat_id)
        await CallbackQuery.message.reply_text("⊱ **sᴛʀᴇᴀᴍ ʀᴇsᴜᴍᴇᴅ** ʙʏ : {} ".format(mention), reply_markup=close_keyboard)

    elif command == "Stop" or command == "End":
        await CallbackQuery.answer()
        await JavaCall.stop_stream(chat_id)
        await set_loop(chat_id, 0)
        await CallbackQuery.message.delete()
        await CallbackQuery.message.reply_text("⊱ **sᴛʀᴇᴀᴍ ᴇɴᴅᴇᴅ/sᴛᴏᴩᴩᴇᴅ** ʙʏ : {} ".format(mention), reply_markup=close_keyboard)
        try:
            popped = check.pop(0)
        except:
            return await CallbackQuery.answer("ꜰᴀɪʟᴇᴅ ᴛᴏ sʜᴜꜰꜰʟᴇ ​.\n\nᴄʜᴇᴄᴋ ǫᴜᴇᴜᴇ : /queue", show_alert=True)
        check = db.get(chat_id)
        if not check:
            check.insert(0, popped)
            return await CallbackQuery.answer("ꜰᴀɪʟᴇᴅ ᴛᴏ sʜᴜꜰꜰʟᴇ ​.\n\nᴄʜᴇᴄᴋ ǫᴜᴇᴜᴇ : /queue", show_alert=True)
        await CallbackQuery.answer()
        random.shuffle(check)
        check.insert(0, popped)
        await CallbackQuery.message.reply_text("**ǫᴜᴇᴜᴇ sʜᴜꜰꜰʟᴇᴅ ʙʏ {0} ​**\n\nᴄʜᴇᴄᴋ sʜᴜꜰꜰʟᴇᴅ ǫᴜᴇᴜᴇ : /queue".format(mention))

    elif command == "Skip":
        check = db.get(chat_id)
        popped = None
        try:
            popped = check.pop(0)
            if popped:
                if AUTO_DOWNLOADS_CLEAR == str(True):
                    await auto_clean(popped)
            if not check:
                await CallbackQuery.edit_message_text("» ꜱᴛʀᴇᴀᴍ ꜱᴋɪᴘᴘᴇᴅ ʙʏ {0}".format(mention), reply_markup=close_keyboard)
                await CallbackQuery.message.reply_text("⊱ sᴛʀᴇᴀᴍ sᴋɪᴩᴩᴇᴅ ʙʏ : {0} \n\n**» ɴᴏ ᴍᴏʀᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ɪɴ** {1}, **ʟᴇᴀᴠɪɴɢ ᴠɪᴅᴇᴏᴄʜᴀᴛ.**".format(mention, CallbackQuery.message.chat.title), reply_markup=close_keyboard)
                try:
                    return await JavaCall.stop_stream(chat_id)
                except:
                    return
        except:
            try:
                await CallbackQuery.edit_message_text("» ꜱᴛʀᴇᴀᴍ ꜱᴋɪᴘᴘᴇᴅ ʙʏ {0}".format(mention), reply_markup=close_keyboard)
                await CallbackQuery.message.reply_text("⊱ sᴛʀᴇᴀᴍ sᴋɪᴩᴩᴇᴅ ʙʏ : {0} \n\n**» ɴᴏ ᴍᴏʀᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ɪɴ** {1}, **ʟᴇᴀᴠɪɴɢ ᴠɪᴅᴇᴏᴄʜᴀᴛ.**".format(mention, CallbackQuery.message.chat.title), reply_markup=close_keyboard)
                return await JavaCall.stop_stream(chat_id)
            except:
                return

        await CallbackQuery.answer()
        queued = check[0]["file"]
        title = (check[0]["title"]).title()
        user = check[0]["by"]
        duration_min = check[0]["dur"]
        streamtype = check[0]["streamtype"]
        videoid = check[0]["vidid"]
        status = True if str(streamtype) == "video" else None
        db[chat_id][0]["played"] = 0

        if "live_" in queued:
            n, link = await YouTube.video(videoid, True)
            if n == 0:
                return await CallbackQuery.message.reply_text("ᴇʀʀᴏʀ ᴡʜɪʟᴇ ᴄʜᴀɴɢɪɴɢ sᴛʀᴇᴀᴍ ᴛᴏ **{0}** ​\n\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴀɢᴀɪɴ.".format(title))
            try:
                await JavaCall.skip_stream(chat_id, link, video=status)
            except Exception:
                return await CallbackQuery.message.reply_text("**ꜰᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ**\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʀᴀᴄᴋ ᴀɢᴀɪɴ.")
            await CallbackQuery.edit_message_text("» ꜱᴛʀᴇᴀᴍ ꜱᴋɪᴘᴘᴇᴅ ʙʏ {0}".format(mention))
            button = telegram_markup(chat_id)
            img = await gen_thumb(videoid)
            run = await CallbackQuery.message.reply_photo(
                photo=img,
                caption="⊱ **Tɪᴛʟᴇ :** [{0}]({1})\n⊱ **Dᴜʀᴀᴛɪᴏɴ :** {2} ᴍɪɴᴜᴛᴇs\n⊱ **Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** {3}".format(user, f"https://t.me/{app.username}?start=info_{videoid}"),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        elif "vid_" in queued:
            mystic = await CallbackQuery.message.reply_text("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ɴᴇxᴛ ᴛʀᴀᴄᴋ ꜰʀᴏᴍ ᴘʟᴀʏʟɪsᴛ", disable_web_page_preview=True)
            try:
                file_path, direct = await YouTube.download(videoid, mystic, videoid=True, video=status)
            except:
                return await mystic.edit_text("**ꜰᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ**\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʀᴀᴄᴋ ᴀɢᴀɪɴ.")
            try:
                await JavaCall.skip_stream(chat_id, file_path, video=status)
            except Exception:
                return await mystic.edit_text("**ꜰᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ**\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʀᴀᴄᴋ ᴀɢᴀɪɴ.")
            await CallbackQuery.edit_message_text("» ꜱᴛʀᴇᴀᴍ ꜱᴋɪᴘᴘᴇᴅ ʙʏ {0}".format(mention))
            button = stream_markup(videoid, chat_id)
            img = await gen_thumb(videoid)
            run = await CallbackQuery.message.reply_photo(
                photo=img,
                caption="⊱ **Tɪᴛʟᴇ :** [{0}]({1})\n⊱ **Dᴜʀᴀᴛɪᴏɴ :** {2} ᴍɪɴᴜᴛᴇs\n⊱ **Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** {3}".format(title[:27], f"https://t.me/{app.username}?start=info_{videoid}", duration_min, user),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
            await mystic.delete()
        elif "index_" in queued:
            try:
                await JavaCall.skip_stream(chat_id, videoid, video=status)
            except Exception:
                return await CallbackQuery.message.reply_text("**ꜰᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ**\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʀᴀᴄᴋ ᴀɢᴀɪɴ.")
            await CallbackQuery.edit_message_text("» ꜱᴛʀᴇᴀᴍ ꜱᴋɪᴘᴘᴇᴅ ʙʏ {0}".format(mention))
            button = telegram_markup(chat_id)
            run = await CallbackQuery.message.reply_photo(
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
                return await CallbackQuery.message.reply_text("**ꜰᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ**\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʀᴀᴄᴋ ᴀɢᴀɪɴ.")
            await CallbackQuery.edit_message_text("» ꜱᴛʀᴇᴀᴍ ꜱᴋɪᴘᴘᴇᴅ ʙʏ {0}".format(mention))
            if videoid == "telegram":
                button = telegram_markup(chat_id)
                run = await CallbackQuery.message.reply_photo(
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
                run = await CallbackQuery.message.reply_photo(
                    photo=img,
                    caption="⊱ **Tɪᴛʟᴇ :** [{0}]({1})\n⊱ **Dᴜʀᴀᴛɪᴏɴ :** {2} ᴍɪɴᴜᴛᴇs\n⊱ **Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** {3}".format(title[:27], f"https://t.me/{app.username}?start=info_{videoid}", duration_min, user),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"

    else:
        playing = db.get(chat_id)
        if not playing:
            return await CallbackQuery.answer("ǫᴜᴇᴜᴇᴅ ʟɪsᴛ ɪs ᴇᴍᴘᴛʏ. ɴᴏ ᴛʀᴀᴄᴋs ғᴏᴜɴᴅ", show_alert=True)

        duration_seconds = int(playing[0]["seconds"])
        if duration_seconds == 0:
            return await CallbackQuery.answer("sᴏʀʀʏ ʙᴜᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ sᴇᴇᴋ ᴛʜᴇ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ, ɪᴛ ᴄᴀɴ ᴏɴʟʏ ʙᴇ sᴋɪᴩᴩᴇᴅ ᴏʀ sᴛᴏᴩᴩᴇᴅ.", show_alert=True)

        file_path = playing[0]["file"]
        if "index_" in file_path or "live_" in file_path:
            return await CallbackQuery.answer("sᴏʀʀʏ ʙᴜᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ sᴇᴇᴋ ᴛʜᴇ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ, ɪᴛ ᴄᴀɴ ᴏɴʟʏ ʙᴇ sᴋɪᴩᴩᴇᴅ ᴏʀ sᴛᴏᴩᴩᴇᴅ.", show_alert=True)

        duration_played = int(playing[0]["played"])
        if int(command) in [1, 2]:
            duration_to_skip = 10
        else:
            duration_to_skip = 30
        duration = playing[0]["dur"]

        if int(command) in [1, 3]:
            if (duration_played - duration_to_skip) <= 10:
                bet = seconds_to_min(duration_played)
                return await CallbackQuery.answer("» ʙᴏᴛ ɪs ᴜɴᴀʙʟᴇ ᴛᴏ sᴇᴇᴋ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇ Dᴜʀᴀᴛɪᴏɴ ᴇxᴄᴇᴇᴅs.\n\nᴄᴜʀʀᴇɴᴛʟʏ ᴩʟᴀʏᴇᴅ :** {0}** ᴍɪɴᴜᴛᴇs ᴏᴜᴛ ᴏғ **{1}** ᴍɪɴᴜᴛᴇs.".format(bet, duration), show_alert=True)
            to_seek = duration_played - duration_to_skip + 1
        else:
            if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
                bet = seconds_to_min(duration_played)
                return await CallbackQuery.answer("» ʙᴏᴛ ɪs ᴜɴᴀʙʟᴇ ᴛᴏ sᴇᴇᴋ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇ Dᴜʀᴀᴛɪᴏɴ ᴇxᴄᴇᴇᴅs.\n\nᴄᴜʀʀᴇɴᴛʟʏ ᴩʟᴀʏᴇᴅ :** {0}** ᴍɪɴᴜᴛᴇs ᴏᴜᴛ ᴏғ **{1}** ᴍɪɴᴜᴛᴇs.".format(bet, duration), show_alert=True)
            to_seek = duration_played + duration_to_skip + 1

        await CallbackQuery.answer()
        mystic = await CallbackQuery.message.reply_text("sᴇᴇᴋɪɴɢ")
        if "vid_" in file_path:
            n, file_path = await YouTube.video(playing[0]["vidid"], True)
            if n == 0:
                return await mystic.edit_text("sᴏʀʀʏ ʙᴜᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ sᴇᴇᴋ ᴛʜᴇ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ, ɪᴛ ᴄᴀɴ ᴏɴʟʏ ʙᴇ sᴋɪᴩᴩᴇᴅ ᴏʀ sᴛᴏᴩᴩᴇᴅ.")
        try:
            await JavaCall.seek_stream(chat_id, file_path, seconds_to_min(to_seek), duration, playing[0]["streamtype"])
        except:
            return await mystic.edit_text("ғᴀɪʟᴇᴅ ᴛᴏ sᴇᴇᴋ")
        if int(command) in [1, 3]:
            db[chat_id][0]["played"] -= duration_to_skip
        else:
            db[chat_id][0]["played"] += duration_to_skip
        string = "sᴇᴇᴋᴇᴅ ᴛᴏ {0} ᴍɪɴs".format(seconds_to_min(to_seek))
        await mystic.edit_text("{0}\n\nᴄʜᴀɴɢᴇs ᴅᴏɴᴇ ʙʏ : {1} !".format(string, mention))
