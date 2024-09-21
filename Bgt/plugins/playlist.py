from os import remove
from config import BANNED_USERS, SERVER_PLAYLIST_LIMIT
from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Bgt.platforms import YouTubeAPI
from Bgt import app
from Bgt.utils.pastebin import Javabin
from Bgt.utils.stream.stream import stream
from Bgt.utils.inline.play import close_keyboard
from Bgt.utils.inline.playlist import botplaylist_markup, get_playlist_markup, warning_markup
from Bgt.utils.database import delete_playlist, get_playlist, get_playlist_names, save_playlist


__MODULE__ = "Pʟᴀʏʟɪsᴛ"
__HELP__ = """
⊱ /playlist : ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴩʟᴀʏʟɪsᴛ ᴏɴ sᴇʀᴠᴇʀs.

⊱ /deleteplaylist : ᴅᴇʟᴇᴛᴇ ᴀɴʏ sᴀᴠᴇᴅ ᴛʀᴀᴄᴋ ɪɴ ʏᴏᴜʀ ᴩʟᴀʏʟɪsᴛ.

⊱ /play : sᴛᴀʀᴛs ᴩʟᴀʏɪɴɢ ғʀᴏᴍ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴩʟᴀʏʟɪsᴛ ᴏɴ sᴇʀᴠᴇʀ
"""


@app.on_message(filters.command(["playlist"]) & ~BANNED_USERS)
async def check_playlist(client, message: Message):
    try:
        await message.delete()
    except:
        pass
    _playlist = await get_playlist_names(message.from_user.id)
    if _playlist:
        get = await message.reply_text("ɢᴇᴛᴛɪɴɢ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ !")
    else:
        return await message.reply_text("ʏᴏᴜ ʜᴀᴠᴇ ɴᴏ ᴘʟᴀʏʟɪsᴛ ᴏɴ ʙᴏᴛ's sᴇʀᴠᴇʀ")
    msg = "ғᴇᴛᴄʜᴇᴅ ᴘʟᴀʏʟɪsᴛ:\n"
    count = 0
    for axen in _playlist:
        _note = await get_playlist(message.from_user.id, axen)
        title = _note["title"].title()
        msg += f"\n\n{count}- {title[:70]}\n"
        msg += "Dᴜʀᴀᴛɪᴏɴ : {0} ᴍɪɴs ".format(_note["duration"])
        count += 1
    link = await Javabin(msg)
    if link:
        await get.edit_text("[Cʜᴇᴄᴋᴏᴜᴛ Wʜᴏʟᴇ Pʟᴀʏʟɪsᴛ]({0})".format(link))
    else:
        ran_hash = f"\\files\Playlist{message.chat.id}{message.from_user.id}.txt"
        with open(ran_hash, "w") as pl:
            pl.write(msg)
        try:
            await message.reply_document(ran_hash, caption="ғᴇᴛᴄʜᴇᴅ ᴘʟᴀʏʟɪsᴛ:\n", file_name=ran_hash)
            await get.delete()
        except Exception as e:
            await get.edit_text("ᴀɴ ᴇxᴄᴇᴘᴛɪᴏɴ ᴏᴄᴄᴜʀᴇᴅ !\n\n{0}".format(str(e)))
        finally:
            remove(ran_hash)


@app.on_message(filters.command(["deleteplaylist"]) & filters.group & ~BANNED_USERS)
async def del_group_message(client, message: Message):
    try:
        await message.delete()
    except:
        pass
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ᴅᴇʟᴇᴛᴇ ᴘʟᴀʏʟɪsᴛ", url=f"https://t.me/{app.username}?start=delplaylists")
            ]
        ]
    )
    await message.reply_text("ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴍ ғᴏʀ ᴅᴇʟᴇᴛɪᴏɴ ᴏғ ᴘʟᴀʏʟɪsᴛs", reply_markup=upl)


async def get_keyboard(user_id):
    keyboard = InlineKeyboard(row_width=5)
    _playlist = await get_playlist_names(user_id)
    count = len(_playlist)
    for x in _playlist:
        _note = await get_playlist(user_id, x)
        title = _note["title"]
        title = title.title()
        keyboard.row(
            InlineKeyboardButton(text=title, callback_data=f"del_playlist {x}")
        )
    keyboard.row(
        InlineKeyboardButton(text="ᴅᴇʟᴇᴛᴇ ᴡʜᴏʟᴇ ᴘʟᴀʏʟɪsᴛ", callback_data="delete_warning"),
        InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data=f"close")
    )
    return keyboard, count


@app.on_message(filters.command(["deleteplaylist"]) & filters.private & ~BANNED_USERS)
async def del_plist_msg(client, message: Message):
    try:
        await message.delete()
    except:
        pass
    _playlist = await get_playlist_names(message.from_user.id)
    if _playlist:
        get = await message.reply_text("ɢᴇᴛᴛɪɴɢ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ !")
    else:
        return await message.reply_text("ʏᴏᴜ ʜᴀᴠᴇ ɴᴏ ᴘʟᴀʏʟɪsᴛ ᴏɴ ʙᴏᴛ's sᴇʀᴠᴇʀ")
    keyboard, count = await get_keyboard(message.from_user.id)
    await get.edit_text("**ᴛʀᴀᴄᴋs ɪɴsɪᴅᴇ ᴘʟᴀʏʟɪsᴛ:** {0}\n\nᴘʀᴇss ᴛʜᴇ ʙᴜᴛᴛᴏɴs ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀ ᴘᴀʀᴛɪᴄᴜʟᴀʀ ᴛʀᴀᴄᴋ ɪɴ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ.\n\n**ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴡʜᴏʟᴇ ᴘʟᴀʏʟɪsᴛ:** ᴘʀᴇss ᴅᴇʟ ᴡʜᴏʟᴇ ᴘʟᴀʏʟɪsᴛ ʙᴜᴛᴛᴏɴ.".format(count), reply_markup=keyboard)


@app.on_callback_query(filters.regex("play_playlist") & ~BANNED_USERS)
async def play_playlist(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    mode = callback_data.split(None, 1)[1]
    user_id = CallbackQuery.from_user.id
    _playlist = await get_playlist_names(user_id)
    if not _playlist:
        try:
            return await CallbackQuery.answer("ʏᴏᴜ ʜᴀᴠᴇ ɴᴏ ᴘʟᴀʏʟɪsᴛ ᴏɴ ʙᴏᴛ's sᴇʀᴠᴇʀ", show_alert=True)
        except:
            return
    chat_id = CallbackQuery.message.chat.id
    user_name = CallbackQuery.from_user.first_name
    await CallbackQuery.message.delete()
    result = []
    try:
        await CallbackQuery.answer()
    except:
        pass
    video = True if mode == "v" else None
    mystic = await CallbackQuery.message.reply_text("🔄 ᴘʀᴏᴄᴇssɪɴɢ ǫᴜᴇʀʏ ")
    for vidids in _playlist:
        result.append(vidids)
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
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else "sᴏᴍᴇ **ᴇxᴄᴇᴘᴛɪᴏɴ ᴏᴄᴄᴜʀᴇᴅ** ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ǫᴜᴇʀʏ\n\nᴇxᴄᴇᴘᴛɪᴏɴ ᴛʏᴘᴇ:- `{0}`".format(ex_type)
        return await mystic.edit_text(err)
    return await mystic.delete()


@app.on_callback_query(filters.regex("add_playlist") & ~BANNED_USERS)
async def add_playlist(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    videoid = callback_data.split(None, 1)[1]
    user_id = CallbackQuery.from_user.id
    _check = await get_playlist(user_id, videoid)
    if _check:
        try:
            return await CallbackQuery.answer("ᴀʟʀᴇᴀᴅʏ ᴇxɪsᴛs\n\nᴛʜɪs ᴛʀᴀᴄᴋ ᴇxɪsᴛs ɪɴ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ.", show_alert=True)
        except:
            return
    _count = await get_playlist_names(user_id)
    count = len(_count)
    if count == SERVER_PLAYLIST_LIMIT:
        try:
            return await CallbackQuery.answer("sᴏʀʀʏ ! ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ ʜᴀᴠᴇ {0} ᴍᴜsɪᴄ ɪɴ ᴀ ᴘʟᴀʏʟɪsᴛ .".format(SERVER_PLAYLIST_LIMIT), show_alert=True)
        except:
            return
    (
        title,
        duration_min,
        duration_sec,
        thumbnail,
        vidid,
    ) = await YouTube.details(videoid, True)
    title = (title[:50]).title()
    plist = {
        "videoid": vidid,
        "title": title,
        "duration": duration_min,
    }
    await save_playlist(user_id, videoid, plist)
    try:
        title = (title[:30]).title()
        return await CallbackQuery.message.reply_text(
            text=" sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴛᴏ ᴩʟᴀʏʟɪsᴛ.\n │\n └Rᴇǫᴜᴇsᴛᴇᴅ Bʏ : {0}".format(CallbackQuery.from_user.mention),
            reply_markup=close_keyboard,
        )
    except:
        return


@app.on_callback_query(filters.regex("del_playlist") & ~BANNED_USERS)
async def del_plist(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    videoid = callback_data.split(None, 1)[1]
    user_id = CallbackQuery.from_user.id
    deleted = await delete_playlist(CallbackQuery.from_user.id, videoid)
    if deleted:
        try:
            await CallbackQuery.answer("sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ʏᴏᴜʀ ᴛʀᴀᴄᴋ", show_alert=True)
        except:
            pass
    else:
        try:
            return await CallbackQuery.answer("ғᴀɪʟᴇᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴛʀᴀᴄᴋ", show_alert=True)
        except:
            return
    keyboard, count = await get_keyboard(user_id)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex("delete_whole_playlist") & ~BANNED_USERS)
async def del_whole_playlist(client, CallbackQuery):
    _playlist = await get_playlist_names(CallbackQuery.from_user.id)
    for x in _playlist:
        await delete_playlist(CallbackQuery.from_user.id, x)
    return await CallbackQuery.edit_message_text("ᴅᴇʟᴇᴛᴇᴅ ʏᴏᴜʀ ᴡʜᴏʟᴇ ᴘʟᴀʏʟɪsᴛs ғʀᴏᴍ ᴛʜᴇ sᴇʀᴠᴇʀ")


@app.on_callback_query(filters.regex("get_playlist_playmode") & ~BANNED_USERS)
async def get_playlist_playmode_(client, CallbackQuery):
    try:
        await CallbackQuery.answer()
    except:
        pass
    buttons = get_playlist_markup()
    return await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex("delete_warning") & ~BANNED_USERS)
async def delete_warning_message(client, CallbackQuery):
    try:
        await CallbackQuery.answer()
    except:
        pass
    upl = warning_markup()
    return await CallbackQuery.edit_message_text("**ᴀʀᴇ ʏᴏᴜ sᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴡʜᴏʟᴇ ᴘʟᴀʏʟɪsᴛ ?**\n\nʏᴏᴜ'ʟʟ ʟᴏsᴛ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ ᴀɴᴅ ᴛʜɪs ᴄᴀɴ'ᴛ ʙᴇ ʀᴇᴄᴏᴠᴇʀᴇᴅ ʟᴀᴛᴇʀ.", reply_markup=upl)


@app.on_callback_query(filters.regex("home_play") & ~BANNED_USERS)
async def home_play_(client, CallbackQuery):
    try:
        await CallbackQuery.answer()
    except:
        pass
    buttons = botplaylist_markup()
    return await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex("del_back_playlist") & ~BANNED_USERS)
async def del_back_playlist(client, CallbackQuery):
    user_id = CallbackQuery.from_user.id
    _playlist = await get_playlist_names(user_id)
    if _playlist:
        try:
            await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ !", show_alert=True)
        except:
            pass
    else:
        try:
            return await CallbackQuery.answer("ʏᴏᴜ ʜᴀᴠᴇ ɴᴏ ᴘʟᴀʏʟɪsᴛ ᴏɴ ʙᴏᴛ's sᴇʀᴠᴇʀ", show_alert=True)
        except:
            return
    keyboard, count = await get_keyboard(user_id)
    return await CallbackQuery.edit_message_text("**ᴛʀᴀᴄᴋs ɪɴsɪᴅᴇ ᴘʟᴀʏʟɪsᴛ:** {0}\n\nᴘʀᴇss ᴛʜᴇ ʙᴜᴛᴛᴏɴs ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀ ᴘᴀʀᴛɪᴄᴜʟᴀʀ ᴛʀᴀᴄᴋ ɪɴ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ.\n\n**ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴡʜᴏʟᴇ ᴘʟᴀʏʟɪsᴛ:** ᴘʀᴇss ᴅᴇʟ ᴡʜᴏʟᴇ ᴘʟᴀʏʟɪsᴛ ʙᴜᴛᴛᴏɴ.".format(count), reply_markup=keyboard)
