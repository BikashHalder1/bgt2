from pyrogram.enums import ChatType
from Bgt import app
from Bgt.misc import SUDOERS
from Bgt.utils.database import get_authuser_names, get_cmode, is_active_chat, is_nonadmin_chat
from config import adminlist
from Bgt.utils.formatters import int_to_alpha


def AdminRightsCheck(mystic):
    async def wrapper(client, message):
        try:
            await message.delete()
        except:
            pass
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await message.reply_text("» ᴘʟᴇᴀsᴇ ᴅᴇғɪɴᴇ ᴄʜᴀɴɴᴇʟ ɪᴅ ᴠɪᴀ /channelplay")
            try:
                await app.get_chat(chat_id)
            except:
                return await message.reply_text("» ᴍᴀᴋᴇ sᴜʀᴇ ʏᴏᴜ'ᴠᴇ ᴀᴅᴅᴇᴅ ᴛʜᴇ ʙᴏᴛ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴘʀᴏᴍᴏᴛᴇᴅ ᴀs ᴀᴅᴍɪɴ !")
        else:
            chat_id = message.chat.id
        if not await is_active_chat(chat_id):
            return await message.reply_text("» ʙᴏᴛ ɪsɴ'ᴛ sᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ !")
        is_non_admin = await is_nonadmin_chat(message.chat.id)
        if not is_non_admin:
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.chat.id)
                if not admins:
                    return
        return await mystic(client, message, chat_id)
    return wrapper


def AdminActual(mystic):
    async def wrapper(client, message):
        try:
            await message.delete()
        except:
            pass
        if message.from_user.id not in SUDOERS:
            try:
                member = (await app.get_chat_member(message.chat.id, message.from_user.id)).privileges
            except AttributeError:
                pass
            except:
                return
            try:
                if not member.can_manage_video_chats:
                    return await message.reply("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs !")
            except AttributeError:
                pass
        return await mystic(client, message)
    return wrapper


def ActualAdminCB(mystic):
    async def wrapper(client, CallbackQuery):
        if CallbackQuery.message.chat.type == ChatType.PRIVATE:
            return await mystic(client, CallbackQuery)
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            try:
                a = (await app.get_chat_member(CallbackQuery.message.chat.id, CallbackQuery.from_user.id)).privileges
            except AttributeError:
                pass
            except:
                return await CallbackQuery.answer("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs !", show_alert=True)
            try:
                if not a.can_manage_video_chats:
                    if CallbackQuery.from_user.id not in SUDOERS:
                        token = await int_to_alpha(CallbackQuery.from_user.id)
                        _check = await get_authuser_names(CallbackQuery.from_user.id)
                        if token not in _check:
                            try:
                                return await CallbackQuery.answer("» ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs !", show_alert=True)
                            except:
                                return
            except AttributeError:
                pass                
            except Exception as e:
                print(e)                
        return await mystic(client, CallbackQuery)
    return wrapper
