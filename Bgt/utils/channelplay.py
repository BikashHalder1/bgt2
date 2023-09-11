from Bgt import app
from Bgt.utils.database import get_cmode


async def get_channeplayCB(command, CallbackQuery):
    if command == "c":
        chat_id = await get_cmode(CallbackQuery.message.chat.id)
        if chat_id is None:
            try:
                return await CallbackQuery.answer("ᴄᴀɴ'ᴛ ᴄʜᴀɴɢᴇ ᴘʟᴀʏ ᴍᴏᴅᴇ ɪɴ ᴀᴄᴛɪᴠᴇ ɢʀᴏᴜᴘ ᴄᴀʟʟ. ᴘʟᴇᴀsᴇ sᴛᴏᴘ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ꜰɪʀsᴛ ᴡɪᴛʜ /stop or /end.", show_alert=True)
            except:
                return
        try:
            chat = await app.get_chat(chat_id)
            channel = chat.title
        except:
            try:
                return await CallbackQuery.answer("ꜰᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ᴄʜᴀɴɴᴇʟ.\n\nᴍᴀᴋᴇ sᴜʀᴇ ʏᴏᴜ ʜᴀᴠᴇ ᴀᴅᴅᴇᴅ ʙᴏᴛ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴘʀᴏᴍᴏᴛᴇᴅ ɪᴛ ᴀs ᴀᴅᴍɪɴ.\nᴇᴅɪᴛ ᴏʀ ᴄʜᴀɴɢᴇ ᴄʜᴀɴɴᴇʟ ᴠɪᴀ /channelplay", show_alert=True)
            except:
                return
    else:
        chat_id = CallbackQuery.message.chat.id
        channel = None
    return chat_id, channel
