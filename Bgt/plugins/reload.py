import asyncio
import time
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import CallbackQuery, Message
from pyrogram.errors import ChatAdminRequired
from config import BANNED_USERS, lyrical
from Bgt import app
from Bgt.misc import db
from Bgt.core.call import JavaCall
from Bgt.utils.database import get_cmode, get_authuser_names
from Bgt.utils.decorators import ActualAdminCB, AdminRightsCheck
from Bgt.utils.formatters import alpha_to_int, get_readable_time
from config import BANNED_USERS, adminlist, lyrical


rel = {}


@app.on_message(filters.group & ~BANNED_USERS, group=17)
async def reload_admin_cache(client, message: Message):
    chat_id = message.chat.id
    try:
        if chat_id not in rel:
            rel[chat_id] = {}
        else:
            saved = rel[message.chat.id]
            if saved > time.time():
                left = get_readable_time((int(saved) - int(time.time())))
                return
        adminlist[chat_id] = []
        async for user in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
            try:
                if user.privileges.can_manage_video_chats:
                    adminlist[chat_id].append(user.user.id)
            except AttributeError:
                pass
        authusers = await get_authuser_names(chat_id)
        for user in authusers:
            user_id = await alpha_to_int(user)
            adminlist[chat_id].append(user_id)
        now = int(time.time()) + 180
        rel[chat_id] = now
    except ChatAdminRequired:
        print("ERROR : Chat Admin Required !")
    except:
        print("ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇʟᴏᴀᴅ ᴀᴅᴍɪɴ ᴄᴀᴄʜᴇ !")


@app.on_message(filters.command(["restart", "reload"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def restartbot(client, message: Message):
    chat_id = message.chat.id
    mystic = await message.reply_text(f"ᴩʟᴇᴀsᴇ ᴡᴀɪᴛ ʀᴇʙᴏᴏᴛɪɴɢ {app.mention} ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ !")
    await asyncio.sleep(1)
    try:
        db[chat_id] = []
        await JavaCall.stop_stream(chat_id)
    except:
        pass
    chat_x = await get_cmode(chat_id)
    if chat_x:
        try:
            await app.get_chat(chat_x)
        except:
            pass
        try:
            db[chat_x] = []
            await JavaCall.stop_stream(chat_x)
        except:
            pass
    return await mystic.edit_text(f"sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇʙᴏᴏᴛᴇᴅ {app.mention} ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ ɴᴏᴡ ʏᴏᴜ ᴄᴀɴ sᴛᴀʀᴛ ᴩʟᴀʏɪɴɢ ᴀɢᴀɪɴ !")


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        return


@app.on_callback_query(filters.regex("stop_downloading") & ~BANNED_USERS)
@ActualAdminCB
async def stop_download(client, CallbackQuery: CallbackQuery):
    message_id = CallbackQuery.message.id
    task = lyrical.get(message_id)

    if not task:
        return await CallbackQuery.answer("ᴅᴏᴡɴʟᴏᴀᴅ ᴀʟʀᴇᴀᴅʏ ᴄᴏᴍᴩʟᴇᴛᴇᴅ.", show_alert=True)
    if task.done() or task.cancelled():
        return await CallbackQuery.answer("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴀʟʀᴇᴀᴅʏ ᴄᴏᴍᴩʟᴇᴛᴇᴅ ᴏʀ ᴄᴀɴᴄᴇʟʟᴇᴅ.", show_alert=True)
    
    if not task.done():
        try:
            task.cancel()
            try:
                lyrical.pop(message_id)
            except:
                pass
            await CallbackQuery.answer("ᴅᴏᴡɴʟᴏᴀᴅɪɢ ᴄᴀɴᴄᴇʟʟᴇᴅ.", show_alert=True)
            return await CallbackQuery.edit_message_text(f"ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴩʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ ʙʏ {CallbackQuery.from_user.mention}")
        except:
            return await CallbackQuery.answer("ғᴀɪʟᴇᴅ ᴛᴏ ᴄᴀɴᴄᴇʟ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...", show_alert=True)
    await CallbackQuery.answer("ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴄᴏɢɴɪᴢᴇ ᴛʜᴇ ᴏɴɢᴏɪɴɢ ᴛᴀsᴋ.", show_alert=True)
