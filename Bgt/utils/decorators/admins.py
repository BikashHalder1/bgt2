from Bgt import app
from Bgt.misc import SUDOERS
from pyrogram.enums import ChatType
from Bgt.utils.database import is_commanddelete_on, is_nonadmin_chat, get_cmode, is_active_chat


def AdminActual(mystic):
    async def wrapper(client, message):
        if await is_commanddelete_on(message.chat.id):
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
        else:
            chat_id = message.chat.id
        if not await is_active_chat(chat_id):
            return await message.reply_text("ʙᴏᴛ ɪsɴ'ᴛ sᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ")

        is_non_admin = await is_nonadmin_chat(message.chat.id)
        if not is_non_admin:
            if message.from_user.id not in SUDOERS:
                try:
                    member = (await app.get_chat_member(message.chat.id, message.from_user.id)).privileges
                except:
                    return
                try:
                    if not member.can_manage_video_chats:
                        return await message.reply("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴡɪᴛʜ **ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ** ʀɪɢʜᴛs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ")
                except AttributeError:
                    pass
        return await mystic(client, message, chat_id)
    return wrapper


def ActualAdminCB(mystic):
    async def wrapper(client, CallbackQuery):
        if CallbackQuery.message.chat.type == ChatType.PRIVATE:
            return await mystic(client, CallbackQuery)
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            if CallbackQuery.from_user.id not in SUDOERS:
                try:
                    a = (await app.get_chat_member(CallbackQuery.message.chat.id, CallbackQuery.from_user.id)).privileges
                except:
                    return 
                try:
                    if not a.can_manage_video_chats:
                        return await CallbackQuery.answer("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ᴡɪᴛʜ **ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ** ʀɪɢʜᴛs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ", show_alert=True)
                except AttributeError:
                    pass
        return await mystic(client, CallbackQuery)
    return wrapper
