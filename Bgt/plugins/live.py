from config import BANNED_USERS
from pyrogram import filters
from Bgt.platforms import YouTube
from Bgt import app
from Bgt.utils.stream.stream import stream
from Bgt.utils.channelplay import get_channeplayCB


@app.on_callback_query(filters.regex("LiveStream") & ~BANNED_USERS)
async def play_live_stream(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    vidid, user_id, mode, cplay, fplay = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer("ᴛʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ ! sᴇᴀʀᴄʜ ʏᴏᴜʀ ᴏᴡɴ sᴏɴɢ", show_alert=True)
        except:
            return
    try:
        chat_id, channel = await get_channeplayCB(cplay, CallbackQuery)
    except:
        return
    video = True if mode == "v" else None
    user_name = CallbackQuery.from_user.first_name
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except:
        pass
    mystic = await CallbackQuery.message.reply_text("🔄 **ᴘʀᴏᴄᴇssɪɴɢ ǫᴜᴇʀʏ** \n\n**ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ:** {0}".format(channel) if channel else "🔄 ᴘʀᴏᴄᴇssɪɴɢ ǫᴜᴇʀʏ ")
    try:
        details, track_id = await YouTube.track(vidid, True)
    except Exception:
        return await mystic.edit_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ !")

    ffplay = True if fplay == "f" else None
    if not details["duration_min"]:
        try:
            await stream(
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                CallbackQuery.message.chat.id,
                video,
                streamtype="live",
                forceplay=ffplay,
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = (
                e
                if ex_type == "AssistantErr"
                else "sᴏᴍᴇ **ᴇxᴄᴇᴘᴛɪᴏɴ ᴏᴄᴄᴜʀᴇᴅ** ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ǫᴜᴇʀʏ\n\nᴇxᴄᴇᴘᴛɪᴏɴ ᴛʏᴘᴇ:- `{0}`".format(ex_type)
            )
            return await mystic.edit_text(err)
    else:
        return await mystic.edit_text("ɪᴛ's ɴᴏᴛ ᴀ ʟɪᴠᴇ sᴛʀᴇᴀᴍ !")
    await mystic.delete()
