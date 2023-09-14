from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from Bgt import app
from config import BANNED_USERS
from Bgt.utils.database import set_cmode
from Bgt.utils.decorators import AdminRightsCheck


@app.on_message(filters.command(["channelplay"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def playmode_(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜsɪᴄ ɪɴ ᴄʜᴀɴɴᴇʟs ꜰʀᴏᴍ ᴛʜɪs ᴄʜᴀᴛ [{0}] ᴛᴏ ᴀɴʏ ᴄʜᴀɴɴᴇʟ ᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ's ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ.\n\n**ꜰᴏʀ ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ:**\n/{1} `linked`\n\n**ꜰᴏʀ ᴀɴʏ ᴏᴛʜᴇʀ ᴄʜᴀɴɴᴇʟ:**\n/{1} [ᴄʜᴀɴɴᴇʟ ɪᴅ]".format(message.chat.title, ["channelplay"][0]))
    query = message.text.split(None, 2)[1].lower().strip()
    if (str(query)).lower() == "disable":
        await set_cmode(message.chat.id, None)
        return await message.reply_text("ᴄʜᴀɴɴᴇʟ ᴩʟᴀʏ ᴅɪsᴀʙʟᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ʙʏ {0} ɪɴ {1}".format(message.from_user.mention, message.chat.title))
    elif str(query) == "linked":
        chat = await app.get_chat(message.chat.id)
        if chat.linked_chat:
            chat_id = chat.linked_chat.id
            await set_cmode(message.chat.id, chat_id)
            return await message.reply_text("ᴄʜᴀɴɴᴇʟ ᴅᴇꜰɪɴᴇᴅ ᴛᴏ {0}\n\nᴄʜᴀɴɴᴇʟ ɪᴅ: {1}".format(chat.linked_chat.title, chat.linked_chat.id))
        else:
            return await message.reply_text("ᴛʜɪs ᴄʜᴀᴛ ʜᴀs ɴᴏ ʟɪɴᴋᴇᴅ ᴄʜᴀɴɴᴇʟ")
    else:
        try:
            chat = await app.get_chat(query)
        except:
            return await message.reply_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ᴄʜᴀɴɴᴇʟ.\n\nᴍᴀᴋᴇ sᴜʀᴇ ʏᴏᴜ ʜᴀᴠᴇ ᴀᴅᴅᴇᴅ ʙᴏᴛ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴘʀᴏᴍᴏᴛᴇᴅ ɪᴛ ᴀs ᴀᴅᴍɪɴ.\nᴇᴅɪᴛ ᴏʀ ᴄʜᴀɴɢᴇ ᴄʜᴀɴɴᴇʟ ᴠɪᴀ /channelplay")
        if chat.type != ChatType.CHANNEL:
            return await message.reply_text("ᴏɴʟʏ ᴄʜᴀɴɴᴇʟs ᴀʀᴇ sᴜᴘᴘᴏʀᴛᴇᴅ")
        try:
            admins = await app.get_chat_members(chat.id, filter=ChatMembersFilter.ADMINISTRATORS)
        except:
            return await message.reply_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ᴄʜᴀɴɴᴇʟ.\n\nᴍᴀᴋᴇ sᴜʀᴇ ʏᴏᴜ ʜᴀᴠᴇ ᴀᴅᴅᴇᴅ ʙᴏᴛ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴘʀᴏᴍᴏᴛᴇᴅ ɪᴛ ᴀs ᴀᴅᴍɪɴ.\nᴇᴅɪᴛ ᴏʀ ᴄʜᴀɴɢᴇ ᴄʜᴀɴɴᴇʟ ᴠɪᴀ /channelplay")
        for user in admins:
            if user.status == ChatMemberStatus.OWNER:
                cusername = user.user.username
                cid = user.user.id
        if cid != message.from_user.id:
            return await message.reply_text("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴛʜᴇ **ᴏᴡɴᴇʀ** ᴏꜰ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ [{0}] ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ɪᴛ ᴡɪᴛʜ ᴛʜɪs ɢʀᴏᴜᴘ.\n**ᴄʜᴀɴɴᴇʟ's ᴏᴡɴᴇʀ:** @{1}\n\nᴀʟᴛᴇʀɴᴀᴛɪᴠᴇʟʏ ʏᴏᴜ ᴄᴀɴ ʟɪɴᴋ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴛᴏ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴛʜᴇɴ ᴛʀʏ ᴄᴏɴɴɴᴇᴄᴛɪɴɢ ᴡɪᴛʜ `/channelplay linked`".format(chat.title, cusername))
        await set_cmode(message.chat.id, chat.id)
        return await message.reply_text("ᴄʜᴀɴɴᴇʟ ᴅᴇꜰɪɴᴇᴅ ᴛᴏ {0}\n\nᴄʜᴀɴɴᴇʟ ɪᴅ: {1}".format(chat.title, chat.id))
