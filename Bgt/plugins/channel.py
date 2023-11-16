from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from Bgt import app
from Bgt.utils.database import set_cmode
from Bgt.utils.decorators import AdminActual



@app.on_message(
    filters.command(["channelplay"])
    & filters.group
    & ~BANNED_USERS
)
@AdminActual
async def playmode_(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "You can play music in channels from this chat[{0}] to any channel or your chat's linked channel.\n\n**For linked channel:**\n`/{1} linked`\n\n**For any other channel:**\n`/{1} [Channel ID]`".format(
                message.chat.title, CHANNELPLAY_COMMAND[0]
            )
        )
    query = message.text.split(None, 2)[1].lower().strip()
    if (str(query)).lower() == "disable":
        await set_cmode(message.chat.id, None)
        return await message.reply_text("Channel Play Disabled")
    elif str(query) == "linked":
        chat = await app.get_chat(message.chat.id)
        if chat.linked_chat:
            chat_id = chat.linked_chat.id
            await set_cmode(message.chat.id, chat_id)
            return await message.reply_text(
                "Channel Defined to {0}\n\n__Channel ID__: {1}".format(
                    chat.linked_chat.title, chat.linked_chat.id
                )
            )
        else:
            return await message.reply_text("This chat has no linked channel.")
    else:
        try:
            chat = await app.get_chat(query)
        except Exception as e:
            print(f"Error: {e}")
            return await message.reply_text("Failed to get channel.\n\nMake sure you have added bot in your channel and promoted it as admin.\nEdit or Change channel via /channelplay")
        if chat.type != ChatType.CHANNEL:
            return await message.reply_text("Only Channels are supported.")
        try:
            async for user in app.get_chat_members(
                chat.id, filter=ChatMembersFilter.ADMINISTRATORS
            ):
                if user.status == ChatMemberStatus.OWNER:
                    creatorusername = user.user.username
                    creatorid = user.user.id
        except Exception as e:
            print(f"Error: {e}")
            return await message.reply_text("Failed to get channel.\n\nMake sure you have added bot in your channel and promoted it as admin.\nEdit or Change channel via /channelplay")
        if creatorid != message.from_user.id:
            return await message.reply_text(
                "You need to be the **Owner** of the channel[{0}] to connect it with this group.\n**Channel's Owner:** @{1}\n\nAlternatively you can link your group to that channel and then try connnecting with `/channelplay linked`".format(chat.title, creatorusername)
            )
        await set_cmode(message.chat.id, chat.id)
        return await message.reply_text(
            "Channel Defined to {0}\n\n__Channel ID__: {1}".format(chat.title, chat.id)
        )
