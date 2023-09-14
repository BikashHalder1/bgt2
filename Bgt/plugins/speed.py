from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import Message
from Bgt import app
from Bgt.misc import db
from Bgt.core.call import JavaCall
from Bgt.utils import AdminRightsCheck
from Bgt.utils.inline.speed import speed_markup
from Bgt.utils.inline.play import close_keyboard
from Bgt.utils.database import is_active_chat


__MODULE__ = "Sᴘᴇᴇᴅ"
__HELP__ = """
⊱ /speed - ɢᴇᴛ sᴏɴɢ ᴘʟᴀʏ sᴘᴇᴇᴅ ᴍᴇɴᴜ

⊱ /speedtest - ɢᴇᴛ sᴘᴇᴇᴅ ᴏғ ʏᴏᴜʀ sᴇʀᴠᴇʀ
"""


checker = []


@app.on_message(filters.command(["speed"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def playback(cli, message: Message, chat_id):
    playing = db.get(chat_id)
    if not playing:
        return await message.reply_text("ǫᴜᴇᴜᴇᴅ ʟɪsᴛ ɪs ᴇᴍᴘᴛʏ. ɴᴏ ᴛʀᴀᴄᴋs ғᴏᴜɴᴅ")
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await message.reply_text("sᴏʀʀʏ ʙᴜᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ sᴘᴇᴇᴅ ᴜᴘ ᴛʜᴇ ᴘʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ")
    file_path = playing[0]["file"]
    if "downloads" not in file_path:
        return await message.reply_text("sᴏʀʀʏ ʙᴜᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ sᴘᴇᴇᴅ ᴜᴘ ᴛʜᴇ ᴘʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ")
    upl = speed_markup(chat_id)
    return await message.reply_text("**{0} sᴘᴇᴇᴅ ʙᴜᴛᴛᴏɴꜱ**\n\nʏᴏᴜ ᴄᴀɴ ᴄʜᴀɴɢᴇ ᴛʜᴇ sᴘᴇᴇᴅ ᴏғ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛʟʏ ᴘʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ᴏɴ ᴠᴄ.".format(app.mention), reply_markup=upl)


@app.on_callback_query(filters.regex("SpeedUP") & ~BANNED_USERS)
async def del_back_playlist(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    chat, speed = callback_request.split("|")
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer("ʙᴏᴛ ɪsɴ'ᴛ sᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ", show_alert=True)
    
    playing = db.get(chat_id)
    if not playing:
        return await CallbackQuery.answer("ǫᴜᴇᴜᴇᴅ ʟɪsᴛ ɪs ᴇᴍᴘᴛʏ. ɴᴏ ᴛʀᴀᴄᴋs ғᴏᴜɴᴅ", show_alert=True)
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await CallbackQuery.answer("sᴏʀʀʏ ʙᴜᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ sᴘᴇᴇᴅ ᴜᴘ ᴛʜᴇ ᴘʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ", show_alert=True)
    file_path = playing[0]["file"]
    if "downloads" not in file_path:
        return await CallbackQuery.answer("sᴏʀʀʏ ʙᴜᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ sᴘᴇᴇᴅ ᴜᴘ ᴛʜᴇ ᴘʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ", show_alert=True)
    checkspeed = (playing[0]).get("speed")

    if checkspeed and (str(checkspeed) == str(speed)):
        if str(speed) == "1.0":
            speed = "ɴᴏʀᴍᴀʟ"
        return await CallbackQuery.answer("ғᴀɪʟᴇᴅ ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʜᴇ sᴘᴇᴇᴅ ᴏғ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ.".format(speed), show_alert=True)
    if chat_id in checker:
        return await CallbackQuery.answer("sᴏᴍᴇᴏɴᴇ ɪs ᴀʟsᴏ ᴛʀʏɪɴɢ ᴛᴏ ᴄᴏɴᴛʀᴏʟ ᴛʜᴇ sᴘᴇᴇᴅ ᴘᴀɴᴇʟ, ʟᴇᴍᴍᴇ ᴄᴏᴍᴘʟᴇᴛᴇ ʜɪs ᴏʀᴅᴇʀ ғɪʀsᴛ", show_alert=True)
    else:
        checker.append(chat_id)
    mystic = await app.send_message(
        CallbackQuery.message.chat.id,
        text="» ᴄʜᴀɴɢɪɴɢ ᴛʜᴇ sᴘᴇᴇᴅ ᴏғ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ.\n\n**ᴄʜᴀɴɢᴇᴅ ʙʏ :** {0}".format(CallbackQuery.from_user.mention),
        reply_markup=close_keyboard
    )
    try:
        await JavaCall.speedup_stream(chat_id, file_path, speed, playing)
    except Exception as e:
        print(e)
        if chat_id in checker:
            checker.remove(chat_id)
        return await mystic.edit_text("ғᴀɪʟᴇᴅ ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʜᴇ sᴘᴇᴇᴅ ᴏғ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ.", reply_markup=close_keyboard)
    if chat_id in checker:
        checker.remove(chat_id)
    await mystic.edit_text("» ᴄʜᴀɴɢᴇᴅ ᴛʜᴇ sᴘᴇᴇᴅ ᴏғ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛʟʏ ᴘʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ᴛᴏ `{0}x`\n\nᴄʜᴀɴɢᴇᴅ ʙʏ : {1}".format(speed, CallbackQuery.from_user.mention), reply_markup=close_keyboard)
