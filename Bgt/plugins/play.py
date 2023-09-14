import random
import string
import config
from config import BANNED_USERS, lyrical
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InputMediaPhoto
from pytgcalls.exceptions import NoActiveGroupCall
from Bgt.core.call import JavaCall
from Bgt.utils.logger import play_logs
from Bgt.utils.formatters import formats
from Bgt.utils.stream.stream import stream
from Bgt.utils import is_served_user, PlayWrapper, served_panel, botplaylist_markup
from Bgt.utils.channelplay import get_channeplayCB
from Bgt.utils import seconds_to_min, time_to_seconds
from Bgt import app
from Bgt.platforms import YouTube, Spotify, Telegram
from Bgt.utils.inline.play import livestream_markup, playlist_markup, slider_markup, track_markup


__MODULE__ = "Mᴜsɪᴄ"
__HELP__ = """
⊱ /play & /bgt ᴏʀ /vplay ᴏʀ /cplay : sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ.
⊱ /playforce ᴏʀ /vplayforce ᴏʀ /cplayforce : **ғᴏʀᴄᴇ ᴩʟᴀʏ** sᴛᴏᴩs ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ.
⊱ /channelplay [ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ] ᴏʀ [ᴅɪsᴀʙʟᴇ] : ᴄᴏɴɴᴇᴄᴛ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴀ ɢʀᴏᴜᴩ ᴀɴᴅ sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʀᴀᴄᴋs ʙʏ ᴛʜᴇ ʜᴇʟᴩ ᴏғ ᴄᴏᴍᴍᴀɴᴅs sᴇɴᴛ ɪɴ ɢʀᴏᴜᴩ
⊱ /pause : ᴩᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.
⊱ /resume : ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴩᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ.
⊱ /restart : ʀᴇsᴛᴀʀᴛ ʙᴏᴛ ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ
⊱ /skip : sᴋɪᴩ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛ sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ɴᴇxᴛ ᴛʀᴀᴄᴋ ɪɴ ǫᴜᴇᴜᴇ.
⊱ /end ᴏʀ /stop : ᴄʟᴇᴀʀs ᴛʜᴇ ǫᴜᴇᴜᴇ ᴀɴᴅ ᴇɴᴅ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.
⊱ /player ᴏʀ /queue : ɢᴇᴛ ᴀɴ ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ ᴩʟᴀʏᴇʀ ᴩᴀɴᴇʟ ᴏʀ sʜᴏᴡs ᴛʜᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ʟɪsᴛ
⊱ /loop [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] ᴏʀ [ʙᴇᴛᴡᴇᴇɴ 1:10] : ᴡʜᴇɴ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ʙᴏᴛ ᴡɪʟʟ ᴩʟᴀʏ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ɪɴ ʟᴏᴏᴩ ғᴏʀ 10 ᴛɪᴍᴇs ᴏʀ ᴛʜᴇ ɴᴜᴍʙᴇʀ ᴏғ ʀᴇǫᴜᴇsᴛᴇᴅ ʟᴏᴏᴩs.
⊱ /shuffle : sʜᴜғғʟᴇ ᴛʜᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs.
⊱ /seek : sᴇᴇᴋ ᴛʜᴇ sᴛʀᴇᴀᴍ ᴛᴏ ᴛʜᴇ ɢɪᴠᴇɴ Dᴜʀᴀᴛɪᴏɴ.
"""


#    This Is For verification Button
 
#    user_id = message.from_user.id
#    keys = served_panel()
#    is_served = await is_served_user(user_id)
#    if not is_served:
#        return


@app.on_message(filters.command(["play", "bgt", "vplay", "cplay", "cvplay", "playforce", "vplayforce", "cplayforce", "cvplayforce"]) & filters.group & ~BANNED_USERS & ~filters.forwarded)
@PlayWrapper
async def play_commnd(client, message: Message, chat_id, video, channel, playmode, url, fplay):
    if message.sender_chat:
        return await message.reply_text("ᴀɴᴏɴʏᴍᴏᴜs ғᴏᴜɴᴅᴇᴅ... ✨\n\nᴘʟᴇᴀsᴇ ʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ᴀᴅᴍɪɴ")
    mystic = await message.reply_text("<b>⊱ ᴄʜᴀɴɴᴇʟ ᴘʟᴀʏ ᴍᴏᴅᴇ</b>\n\nᴘʀᴏᴄᴇssɪɴɢ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ\n\n<b>ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ :</b> {0}".format(channel) if channel else "🔄 ᴘʀᴏᴄᴇssɪɴɢ ǫᴜᴇʀʏ")
    plist_id = None
    slider = None
    plist_type = None
    spotify = None
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    audio_telegram = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    video_telegram = (
        (message.reply_to_message.video or message.reply_to_message.document)
        if message.reply_to_message
        else None
    )
    
    if audio_telegram:
        if audio_telegram.file_size > 104857600:
            return await mystic.edit_text("» ᴀᴜᴅɪᴏ ғɪʟᴇ sɪᴢᴇ ɪs ʟᴀʀɢᴇʀ ᴛʜᴀɴ ᴛʜᴇ ᴅᴇғɪɴᴇᴅ ʟɪᴍɪᴛ")
        duration_min = seconds_to_min(audio_telegram.duration)   
        if (audio_telegram.duration) > config.DURATION_LIMIT:
            return await mystic.edit_text("» sᴛʀᴇᴀᴍ's ʟᴏɴɢᴇʀ ᴛʜᴀɴ {0} ᴀʀᴇɴ'ᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ ᴏɴ {1}".format(config.DURATION_LIMIT_MIN, app.mention))
        file_path = await Telegram.get_filepath(audio=audio_telegram)      
        if await Telegram.download(message, mystic, file_path):
            message_link = await Telegram.get_link(message)
            file_name = await Telegram.get_filename(audio_telegram, audio=True)
            dur = await Telegram.get_duration(audio_telegram, file_path)
            details = {"title": file_name, "link": message_link, "path": file_path, "dur": dur,}
            try:
                await stream(mystic, user_id, details, chat_id, user_name, message.chat.id, streamtype="telegram", forceplay=fplay)
            except Exception as e:
                ex_type = type(e).__name__
                err = e if ex_type == "AssistantErr" else "» sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ǫᴜᴇʀʏ.\n\nᴇxᴄᴇᴘᴛɪᴏɴ : <code>{0}</code>".format(ex_type)
                return await mystic.edit_text(err)
            return await mystic.delete()
        return
    
    elif video_telegram:
        if message.reply_to_message.document:
            try:
                ext = video_telegram.file_name.split(".")[-1]
                if ext.lower() not in formats:
                    return await mystic.edit_text("» ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ ᴠɪᴅᴇᴏ ғɪʟᴇ ᴇxᴛᴇɴsɪᴏɴ.")
            except:
                return await mystic.edit_text("» ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ ᴠɪᴅᴇᴏ ғɪʟᴇ ᴇxᴛᴇɴsɪᴏɴ.")
        if video_telegram.file_size > config.TG_VIDEO_FILESIZE_LIMIT:
            return await mystic.edit_text("» ᴠɪᴅᴇᴏ ғɪʟᴇ sɪᴢᴇ sʜᴏᴜʟᴅ ʙᴇ ʟᴇss ᴛʜᴀɴ 1ɢɪʙ")
        file_path = await Telegram.get_filepath(video=video_telegram)
        if await Telegram.download(message, mystic, file_path):
            message_link = await Telegram.get_link(message)
            file_name = await Telegram.get_filename(video_telegram)
            dur = await Telegram.get_duration(video_telegram, file_path)
            details = {"title": file_name, "link": message_link, "path": file_path, "dur": dur}
            try:
                await stream(mystic, user_id, details, chat_id, user_name, message.chat.id, video=True, streamtype="telegram", forceplay=fplay)
            except Exception as e:
                ex_type = type(e).__name__
                err = e if ex_type == "AssistantErr" else "» sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ǫᴜᴇʀʏ.\n\nᴇxᴄᴇᴘᴛɪᴏɴ : <code>{0}</code>".format(ex_type)
                return await mystic.edit_text(err)
            return await mystic.delete()
        return
    
    elif url:
        if await YouTube.exists(url):
            if "playlist" in url:
                try:
                    details = await YouTube.playlist(url, config.PLAYLIST_FETCH_LIMIT, message.from_user.id)
                except:
                    return await mystic.edit_text("» ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ")
                streamtype = "playlist"
                plist_type = "yt"
                if "&" in url:
                    plist_id = (url.split("=")[1]).split("&")[0]
                else:
                    plist_id = url.split("=")[1]
                img = config.STREAM_IMG
                cap = "<b><u>ʏᴏᴜᴛᴜʙᴇ ᴘʟᴀʏʟɪsᴛ ғᴇᴀᴛᴜʀᴇ</b></u>\n\nsᴇʟᴇᴄᴛ ᴛʜᴇ ᴍᴏᴅᴇ ɪɴ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴘʟᴀʏ ᴡʜᴏʟᴇ ʏᴏᴜᴛᴜʙᴇ ᴘʟᴀʏʟɪsᴛ."
            else:
                try:
                    details, track_id = await YouTube.track(url)
                except:
                    return await mystic.edit_text("» ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ")
                streamtype = "youtube"
                img = details["thumb"]
                cap = "<b>Tɪᴛʟᴇ :</b> {0}\n<b>Dᴜʀᴀᴛɪᴏɴ :</b> {1} ᴍɪɴᴜᴛᴇs".format(details["title"], details["duration_min"])
                
        elif await Spotify.valid(url):
            spotify = True
            if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
                return await mystic.edit_text("» sᴘᴏᴛɪғʏ ɪs ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ ʏᴇᴛ.")
            if "track" in url:
                try:
                    details, track_id = await Spotify.track(url)
                except:
                    return await mystic.edit_text("» ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ")
                streamtype = "youtube"
                img = details["thumb"]
                cap = "<b>Tɪᴛʟᴇ :</b> {0}\n<b>Dᴜʀᴀᴛɪᴏɴ :</b> {1} ᴍɪɴᴜᴛᴇs".format(details["title"], details["duration_min"])
            elif "playlist" in url:
                try:
                    details, plist_id = await Spotify.playlist(url)
                except Exception:
                    return await mystic.edit_text("» ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ")
                streamtype = "playlist"
                plist_type = "spplay"
                img = config.STREAM_IMG
                cap = "<u><b>{0} sᴘᴏᴛɪғʏ ᴘʟᴀʏᴇʀ</b></u>\n\n<b>Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :</b> {1}".format(app.mention, message.from_user.mention)
            elif "album" in url:
                try:
                    details, plist_id = await Spotify.album(url)
                except:
                    return await mystic.edit_text("» ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ")
                streamtype = "playlist"
                plist_type = "spalbum"
                img = config.STREAM_IMG
                cap = "<u><b>{0} sᴘᴏᴛɪғʏ ᴘʟᴀʏᴇʀ</b></u>\n\n<b>Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :</b> {1}".format(app.mention, message.from_user.mention)
            elif "artist" in url:
                try:
                    details, plist_id = await Spotify.artist(url)
                except:
                    return await mystic.edit_text("» ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ")
                streamtype = "playlist"
                plist_type = "spartist"
                img = config.STREAM_IMG
                cap = "<u><b>{0} sᴘᴏᴛɪғʏ ᴘʟᴀʏᴇʀ</b></u>\n\n<b>Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :</b> {1}".format(message.from_user.first_name)
            else:
                return await mystic.edit_text("» ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ.")
    
        else:
            try:
                await JavaCall.stream_call(url)
            except NoActiveGroupCall:
                await mystic.edit_text("» ᴘʟᴇᴀsᴇ ᴛᴜʀɴ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ")
            except Exception as e:
                return await mystic.edit_text("» sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ǫᴜᴇʀʏ.\n\nᴇxᴄᴇᴘᴛɪᴏɴ : <code>{0}</code>".format(type(e).__name__))
            await mystic.edit_text("⊱ ᴘʀᴏᴄᴇssɪɴɢ")
            try:
                await stream(mystic, message.from_user.id, url, chat_id, message.from_user.first_name, message.chat.id, video=video, streamtype="index", forceplay=fplay)
            except Exception as e:
                ex_type = type(e).__name__
                err = e if ex_type == "AssistantErr" else "» sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ǫᴜᴇʀʏ.\n\nᴇxᴄᴇᴘᴛɪᴏɴ : <code>{0}</code>".format(ex_type)
                return await mystic.edit_text(err)
            return await play_logs(message, streamtype="M3u8 or Index Link")

    else:
        if len(message.command) < 2:
            buttons = botplaylist_markup()
            return await mystic.edit_text("<b>ᴜsᴀɢᴇ :</b> /play [sᴏɴɢ ɴᴀᴍᴇ/ʏᴏᴜᴛᴜʙᴇ ᴜʀʟ/ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴀᴜᴅɪᴏ/ᴠɪᴅᴇᴏ ғɪʟᴇ]", reply_markup=InlineKeyboardMarkup(buttons))
        slider = True
        query = message.text.split(None, 1)[1]
        if "-v" in query:
            query = query.replace("-v", "")
        try:
            details, track_id = await YouTube.track(query)
        except:
            return await mystic.edit_text("» ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ")
        streamtype = "youtube"

    if str(playmode) == "Direct":
        if not plist_type:
            if details["duration_min"]:
                duration_sec = time_to_seconds(details["duration_min"])
                if duration_sec > config.DURATION_LIMIT:
                    return await mystic.edit_text("» sᴛʀᴇᴀᴍ's ʟᴏɴɢᴇʀ ᴛʜᴀɴ {0} ᴀʀᴇɴ'ᴛ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ ᴏɴ {1}".format(config.DURATION_LIMIT_MIN, app.mention))
            else:
                buttons = livestream_markup(track_id, user_id, "v" if video else "a", "c" if channel else "g", "f" if fplay else "d")
                return await mystic.edit_text("» ʟɪᴠᴇ sᴛʀᴇᴀᴍ ᴅᴇᴛᴇᴄᴛᴇᴅ.", reply_markup=InlineKeyboardMarkup(buttons))
        try:
            await stream(mystic, user_id, details, chat_id, user_name, message.chat.id, video=video, streamtype=streamtype, spotify=spotify, forceplay=fplay)
        except Exception as e:
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else "» sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ǫᴜᴇʀʏ.\n\nᴇxᴄᴇᴘᴛɪᴏɴ : <code>{0}</code>".format(ex_type)
            return await mystic.edit_text(err)
        await mystic.delete()
        return await play_logs(message, streamtype=streamtype)
    
    else:
        if plist_type:
            ran_hash = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
            lyrical[ran_hash] = plist_id
            buttons = playlist_markup(ran_hash, message.from_user.id, plist_type, "c" if channel else "g", "f" if fplay else "d")
            await mystic.delete()
            await message.reply_photo(photo=img, caption=cap,reply_markup=InlineKeyboardMarkup(buttons))
            return await play_logs(message, streamtype=f"Playlist : {plist_type}")
        else:
            if slider:
                buttons = slider_markup(track_id, message.from_user.id, query, 0, "c" if channel else "g", "f" if fplay else "d")
                await mystic.delete()
                await message.reply_photo(
                    photo=details["thumb"],
                    caption="<b>Tɪᴛʟᴇ :</b> {0}\n<b>Dᴜʀᴀᴛɪᴏɴ :</b> {1} ᴍɪɴᴜᴛᴇs".format(details["title"].title(), details["duration_min"]),
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
                return await play_logs(message, streamtype=f"Searched on Youtube")
            else:
                buttons = track_markup(track_id, message.from_user.id, "c" if channel else "g", "f" if fplay else "d")
                await mystic.delete()
                await message.reply_photo(
                    photo=img,
                    caption=cap,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
                return await play_logs(message, streamtype=f"URL Searched Inline")


@app.on_callback_query(filters.regex("MusicStream") & ~BANNED_USERS)
async def play_music(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    vidid, user_id, mode, cplay, fplay = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer("ᴛʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ ! sᴇᴀʀᴄʜ ʏᴏᴜʀ ᴏᴡɴ sᴏɴɢ", show_alert=True)
        except:
            return
    try:
        chat_id, channel = await get_channeplayCB(
            cplay, CallbackQuery
        )
    except:
        return
    user_name = CallbackQuery.from_user.first_name
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        pass
    mystic = await CallbackQuery.message.reply_text(
        "🏷**ᴄʜᴀɴɴᴇʟ ᴘʟᴀʏ ᴍᴏᴅᴇ**\n🔄 ᴘʀᴏᴄᴇssɪɴɢ ǫᴜᴇʀʏ \n\n**ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ:** {0}".format(channel) if channel else "🔄 ᴘʀᴏᴄᴇssɪɴɢ ǫᴜᴇʀʏ "
    )
    try:
        details, track_id = await YouTube.track(vidid, True)
    except Exception:
        return await mystic.edit_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ !")
    if details["duration_min"]:
        duration_sec = time_to_seconds(details["duration_min"])
        if duration_sec > config.DURATION_LIMIT:
            return await mystic.edit_text(
                "**Dᴜʀᴀᴛɪᴏɴ ʟɪᴍɪᴛ ᴇxᴄᴇᴇᴅᴇᴅ**\n\n**ᴀʟʟᴏᴡᴇᴅ Dᴜʀᴀᴛɪᴏɴ:** {0} ᴍɪɴᴜᴛᴇs\n**ʀᴇᴄᴇɪᴠᴇᴅ Dᴜʀᴀᴛɪᴏɴ:** {1} ᴍɪɴᴜᴛᴇs".format(config.DURATION_LIMIT_MIN, details["duration_min"])
            )
    else:
        buttons = livestream_markup(
            track_id,
            CallbackQuery.from_user.id,
            mode,
            "c" if cplay == "c" else "g",
            "f" if fplay else "d",
        )
        return await mystic.edit_text("**ʟɪᴠᴇ sᴛʀᴇᴀᴍ ᴅᴇᴛᴇᴄᴛᴇᴅ**", reply_markup=InlineKeyboardMarkup(buttons))
    video = True if mode == "v" else None
    ffplay = True if fplay == "f" else None
    try:
        await stream(
            mystic,
            CallbackQuery.from_user.id,
            details,
            chat_id,
            user_name,
            CallbackQuery.message.chat.id,
            video,
            streamtype="youtube",
            forceplay=ffplay,
        )
    except Exception as e:
        print(f"Error: {e}")
        ex_type = type(e).__name__
        err = (
            e
            if ex_type == "AssistantErr"
            else "sᴏᴍᴇ **ᴇxᴄᴇᴘᴛɪᴏɴ ᴏᴄᴄᴜʀᴇᴅ** ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ǫᴜᴇʀʏ\n\nᴇxᴄᴇᴘᴛɪᴏɴ ᴛʏᴘᴇ:- `{0}`".format(ex_type)
        )
        return await mystic.edit_text(err)
    return await mystic.delete()


@app.on_callback_query(filters.regex("JavaPlaylists") & ~BANNED_USERS)
async def play_playlists_command(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    (
        videoid,
        user_id,
        ptype,
        mode,
        cplay,
        fplay,
    ) = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer("ᴛʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ ! sᴇᴀʀᴄʜ ʏᴏᴜʀ ᴏᴡɴ sᴏɴɢ", show_alert=True)
        except:
            return
    try:
        chat_id, channel = await get_channeplayCB(cplay, CallbackQuery)
    except:
        return
    user_name = CallbackQuery.from_user.first_name
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except:
        pass
    mystic = await CallbackQuery.message.reply_text("🏷**ᴄʜᴀɴɴᴇʟ ᴘʟᴀʏ ᴍᴏᴅᴇ**\n🔄 ᴘʀᴏᴄᴇssɪɴɢ ǫᴜᴇʀʏ \n\n**ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ:** {0}".format(channel) if channel else "🔄 ᴘʀᴏᴄᴇssɪɴɢ ǫᴜᴇʀʏ ")
    videoid = lyrical.get(videoid)
    video = True if mode == "v" else None
    ffplay = True if fplay == "f" else None
    spotify = True
    if ptype == "yt":
        spotify = False
        try:
            result = await YouTube.playlist(
                videoid,
                config.PLAYLIST_FETCH_LIMIT,
                CallbackQuery.from_user.id,
                True,
            )
        except Exception:
            return await mystic.edit_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ !")
    if ptype == "spplay":
        try:
            result, spotify_id = await Spotify.playlist(videoid)
        except Exception:
            return await mystic.edit_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ !")
    elif ptype == "spalbum":
        try:
            result, spotify_id = await Spotify.album(videoid)
        except Exception:
            return await mystic.edit_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ !")
    elif ptype == "spartist":
        try:
            result, spotify_id = await Spotify.artist(videoid)
        except Exception:
            return await mystic.edit_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ !")
    try:
        await stream(
            mystic,
            user_id,
            result,
            chat_id,
            user_name,
            CallbackQuery.message.chat.id,
            video,
            streamtype="playlist",
            spotify=spotify,
            forceplay=ffplay,
        )
    except Exception as e:
        print(f"Error: {e}")
        ex_type = type(e).__name__
        err = (
            e
            if ex_type == "AssistantErr"
            else "sᴏᴍᴇ **ᴇxᴄᴇᴘᴛɪᴏɴ ᴏᴄᴄᴜʀᴇᴅ** ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ǫᴜᴇʀʏ\n\nᴇxᴄᴇᴘᴛɪᴏɴ ᴛʏᴘᴇ:- `{0}`".format(ex_type)
        )
        return await mystic.edit_text(err)
    return await mystic.delete()


@app.on_callback_query(filters.regex("slider") & ~BANNED_USERS)
async def slider_queries(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    (
        what,
        rtype,
        query,
        user_id,
        cplay,
        fplay,
    ) = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer("ᴛʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ ! sᴇᴀʀᴄʜ ʏᴏᴜʀ ᴏᴡɴ sᴏɴɢ", show_alert=True)
        except:
            return
    what = str(what)
    rtype = int(rtype)
    if what == "F":
        if rtype == 9:
            query_type = 0
        else:
            query_type = int(rtype + 1)
        try:
            await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ɴᴇxᴛ ʀᴇsᴜʟᴛ")
        except:
            pass
        title, duration_min, thumbnail, vidid = await YouTube.slider(query, query_type)
        buttons = slider_markup(vidid, user_id, query, query_type, cplay, fplay)
        med = InputMediaPhoto(media=thumbnail, caption="⊱ **Tɪᴛʟᴇ:** {0}\n\n⊱ **Dᴜʀᴀᴛɪᴏɴ:** {1} ᴍɪɴs".format(title.title(), duration_min))
        return await CallbackQuery.edit_message_media(media=med, reply_markup=InlineKeyboardMarkup(buttons))
    elif what == "B":
        if rtype == 0:
            query_type = 9
        else:
            query_type = int(rtype - 1)
        try:
            await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ɴᴇxᴛ ʀᴇsᴜʟᴛ")
        except:
            pass
        title, duration_min, thumbnail, vidid = await YouTube.slider(query, query_type)
        buttons = slider_markup(vidid, user_id, query, query_type, cplay, fplay)
        med = InputMediaPhoto(media=thumbnail, caption="⊱ **Tɪᴛʟᴇ:** {0}\n\n⊱ **Dᴜʀᴀᴛɪᴏɴ:** {1} ᴍɪɴs".format(title.title(), duration_min))
        return await CallbackQuery.edit_message_media(media=med, reply_markup=InlineKeyboardMarkup(buttons))
