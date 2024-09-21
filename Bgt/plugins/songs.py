import os
import re
import yt_dlp
from pykeyboard import InlineKeyboard
from config import BANNED_USERS, SONG_DOWNLOAD_DURATION, SONG_DOWNLOAD_DURATION_LIMIT
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaAudio, InputMediaVideo, Message
from Bgt.platforms import YouTubeAPI
from Bgt import app
from Bgt.utils.inline.song import song_markup
from Bgt.utils.formatters import convert_bytes


__MODULE__ = "Sᴏɴɢ"
__HELP__ = """
⊱ /song - ᴅᴏᴡɴʟᴏᴀᴅ ɢɪᴠᴇɴ sᴏɴɢ

⊱ /video - ᴅᴏᴡɴʟᴏᴀᴅ ɢɪᴠᴇɴ ᴠɪᴅᴇᴏ
"""


@app.on_message(filters.command(["song", "video"]) & ~BANNED_USERS)
async def song_commad_private(client, message: Message):
    try:
        await message.delete()
    except:
        pass
    url = await YouTube.url(message)
    if url:
        if not await YouTube.exists(url):
            return await message.reply_text("ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ.")
        mystic = await message.reply_text("🔄 ᴘʀᴏᴄᴇssɪɴɢ ǫᴜᴇʀʏ ")
        (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        ) = await YouTube.details(url)
        if str(duration_min) == "None":
            return await mystic.edit_text("ʟɪᴠᴇ ʟɪɴᴋ ᴅᴇᴛᴇᴄᴛᴇᴅ. ɪ ᴀᴍ ɴᴏᴛ ᴀʙʟᴇ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪᴠᴇ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏs")
        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(
                "🖇 **ᴀᴅᴍɪɴs ᴏɴʟʏ ᴘʟᴀʏ**\nᴏɴʟʏ ᴀᴅᴍɪɴs ᴀɴᴅ ᴀᴜᴛʜ ᴜsᴇʀs ᴄᴀɴ ᴘʟᴀʏ ᴍᴜsɪᴄ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.\n\nᴄʜᴀɴɢᴇ ᴍᴏᴅᴇ ᴠɪᴀ /playmode ᴀɴᴅ ɪꜰ ʏᴏᴜ'ʀᴇ ᴀʟʀᴇᴀᴅʏ ᴀᴅᴍɪɴ, ʀᴇʟᴏᴀᴅ ᴀᴅᴍɪɴᴄᴀᴄʜᴇ ᴠɪᴀ /reload".format(SONG_DOWNLOAD_DURATION, duration_min)
            )
        buttons = song_markup(vidid)
        await mystic.delete()
        return await message.reply_photo(
            thumbnail,
            caption="⊱**Tɪᴛʟᴇ**:- {0}\n\nsᴇʟᴇᴄᴛ ᴛʜᴇ ᴛʏᴘᴇ ɪɴ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ".format(title),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            return await message.reply_text("**ᴜsᴀɢᴇ:**\n\n/song [ᴍᴜsɪᴄ ɴᴀᴍᴇ] ᴏʀ [ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ]")
    mystic = await message.reply_text("🔄 ᴘʀᴏᴄᴇssɪɴɢ ǫᴜᴇʀʏ ")
    query = message.text.split(None, 1)[1]
    try:
        (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        ) = await YouTube.details(query)
    except:
        return await mystic.edit_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ !")
    if str(duration_min) == "None":
        return await mystic.edit_text("ʟɪᴠᴇ ʟɪɴᴋ ᴅᴇᴛᴇᴄᴛᴇᴅ. ɪ ᴀᴍ ɴᴏᴛ ᴀʙʟᴇ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪᴠᴇ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏs")
    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(
            "**Dᴜʀᴀᴛɪᴏɴ ʟɪᴍɪᴛ ᴇxᴄᴇᴇᴅᴇᴅ**\n\n**ᴀʟʟᴏᴡᴇᴅ Dᴜʀᴀᴛɪᴏɴ:** {0} ᴍɪɴᴜᴛᴇs\n**ʀᴇᴄᴇɪᴠᴇᴅ Dᴜʀᴀᴛɪᴏɴ:** {1} ᴍɪɴᴜᴛᴇs".format(SONG_DOWNLOAD_DURATION, duration_min)
        )
    buttons = song_markup(vidid)
    await mystic.delete()
    return await message.reply_photo(
        thumbnail,
        caption="⊱**Tɪᴛʟᴇ**:- {0}\n\nsᴇʟᴇᴄᴛ ᴛʜᴇ ᴛʏᴘᴇ ɪɴ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ".format(title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex(pattern=r"song_back") & ~BANNED_USERS)
async def songs_back_helper(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    buttons = song_markup(vidid)
    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"song_helper") & ~BANNED_USERS)
async def song_helper_cb(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    try:
        await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ꜰᴏʀᴍᴀᴛs ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ", show_alert=True)
    except:
        pass
    if stype == "audio":
        try:
            formats_available, link = await YouTube.formats(vidid, True)
        except:
            return await CallbackQuery.edit_message_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ꜰᴏʀᴍᴀᴛs ꜰᴏʀ ᴛʜᴇ ᴠɪᴅᴇᴏ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɴʏ ᴏᴛʜᴇʀ ᴛʀᴀᴄᴋ.")
        keyboard = InlineKeyboard()
        done = []
        for x in formats_available:
            check = x["format"]
            if "audio" in check:
                if x["filesize"] is None:
                    continue
                form = x["format_note"].title()
                if form not in done:
                    done.append(form)
                else:
                    continue
                sz = convert_bytes(x["filesize"])
                fom = x["format_id"]
                keyboard.row(
                    InlineKeyboardButton(
                        text=f"{form} Quality Audio = {sz}",
                        callback_data=f"song_download {stype}|{fom}|{vidid}",
                    ),
                )
        keyboard.row(
            InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data=f"song_back {stype}|{vidid}"),
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data=f"close")
        )
        return await CallbackQuery.edit_message_reply_markup(keyboard)
    else:
        try:
            formats_available, link = await YouTube.formats(vidid, True)
        except Exception as e:
            print(e)
            return await CallbackQuery.edit_message_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ꜰᴏʀᴍᴀᴛs ꜰᴏʀ ᴛʜᴇ ᴠɪᴅᴇᴏ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɴʏ ᴏᴛʜᴇʀ ᴛʀᴀᴄᴋ.")
        keyboard = InlineKeyboard()
        done = [160, 133, 134, 135, 136, 137, 298, 299, 264, 304, 266]
        for x in formats_available:
            check = x["format"]
            if x["filesize"] is None:
                continue
            if int(x["format_id"]) not in done:
                continue
            sz = convert_bytes(x["filesize"])
            ap = check.split("-")[1]
            to = f"{ap} = {sz}"
            keyboard.row(
                InlineKeyboardButton(text=to, callback_data=f"song_download {stype}|{x['format_id']}|{vidid}")
            )
        keyboard.row(
            InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data=f"song_back {stype}|{vidid}"),
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data=f"close")
        )
        return await CallbackQuery.edit_message_reply_markup(keyboard)


@app.on_callback_query(filters.regex(pattern=r"song_download") & ~BANNED_USERS)
async def song_download_cb(client, CallbackQuery):
    try:
        await CallbackQuery.answer("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")
    except:
        pass
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, format_id, vidid = callback_request.split("|")
    mystic = await CallbackQuery.edit_message_text("ᴅᴏᴡɴʟᴏᴀᴅ sᴛᴀʀᴛᴇᴅ")
    yturl = f"https://www.youtube.com/watch?v={vidid}"
    with yt_dlp.YoutubeDL({"quiet": True}) as ytdl:
        x = ytdl.extract_info(yturl, download=False)
    title = (x["title"]).title()
    title = re.sub("\W+", " ", title)
    thumb_image_path = await CallbackQuery.message.download()
    duration = x["duration"]

    if stype == "video":
        thumb_image_path = await CallbackQuery.message.download()
        width = CallbackQuery.message.photo.width
        height = CallbackQuery.message.photo.height
        try:
            file_path = await YouTube.download(
                yturl,
                mystic,
                songvideo=True,
                format_id=format_id,
                title=title,
            )
        except Exception as e:
            return await mystic.edit_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ sᴏɴɢ ꜰʀᴏᴍ ʏᴛ-ᴅʟ\n\n**ʀᴇᴀsᴏɴ:** {0}".format(e))
        med = InputMediaVideo(
            media=file_path,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb_image_path,
            caption=title,
            supports_streaming=True,
        )
        await mystic.edit_text("ᴜᴘʟᴏᴀᴅɪɴɢ sᴛᴀʀᴛᴇᴅ")
        try:
            await CallbackQuery.edit_message_media(media=med)
        except Exception as e:
            print(e)
            return await mystic.edit_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴜᴘʟᴏᴀᴅ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ sᴇʀᴠᴇʀs")
        os.remove(file_path)

    elif stype == "audio":
        try:
            filename = await YouTube.download(
                yturl,
                mystic,
                songaudio=True,
                format_id=format_id,
                title=title,
            )
        except Exception as e:
            return await mystic.edit_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ sᴏɴɢ ꜰʀᴏᴍ ʏᴛ-ᴅʟ\n\n**ʀᴇᴀsᴏɴ:** {0}".format(e))
        med = InputMediaAudio(
            media=filename,
            caption=title,
            thumb=thumb_image_path,
            title=title,
            performer=x["uploader"],
        )
        await mystic.edit_text("ᴜᴘʟᴏᴀᴅɪɴɢ sᴛᴀʀᴛᴇᴅ")
        try:
            await CallbackQuery.edit_message_media(media=med)
        except Exception as e:
            print(e)
            return await mystic.edit_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴜᴘʟᴏᴀᴅ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ sᴇʀᴠᴇʀs")
        os.remove(filename)
