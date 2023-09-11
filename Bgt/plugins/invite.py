from config import LOG_GROUP_ID
from Bgt import app
from Bgt.misc import SUDOERS
from pyrogram import filters
from pyrogram.errors import PeerIdInvalid


@app.on_message(filters.command(["invite", "link"]) & SUDOERS)
async def invitee_link(_, message):
    try:
        await message.delete()
    except:
        pass
    try:
        if len(message.command) == 2:
            chat_id = message.command[1]
        else:
            chat_id = message.chat.id
        
        await app.resolve_peer(chat_id)
        chat = await app.get_chat(chat_id)
        link = chat.invite_link
        if not link:
            link = await app.export_chat_invite_link(chat_id)

        text = f"ɢʀᴏᴜᴘ ɪɴᴠɪᴛᴇ ʟɪɴᴋ :\n\n{link}"

        if message.reply_to_message:
            await message.reply_to_message.reply_text(text, disable_web_page_preview=True)
        else:
            await message.reply_text(text, disable_web_page_preview=True)
    except (IndexError, AttributeError):
        pass                
    except PeerIdInvalid:
        await app.send_message(LOG_GROUP_ID, "ᴍᴀᴋᴇ sᴜʀᴇ ʏᴏᴜ ʜᴀᴠᴇ ᴊᴏɪɴᴇᴅ ᴛʜɪs ɢʀᴏᴜᴘ ʙᴇғᴏʀᴇ ᴏʀ ɢɪᴠᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ғʀᴏᴍ ʏᴏᴜʀ ᴍᴜsɪᴄ ᴀssɪsᴛᴀɴᴛ ɪᴅ !")
