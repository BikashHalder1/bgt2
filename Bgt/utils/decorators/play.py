import asyncio
from config import adminlist, BIKASH_IMG
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import ChatAdminRequired, InviteRequestSent, UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup
from Bgt import app, YouTubeAPI
from Bgt.misc import SUDOERS
from Bgt.utils.database import get_cmode, get_playmode, get_playtype, is_active_chat, get_assistant
from Bgt.utils.inline.playlist import botplaylist_markup


links = {}


def PlayWrapper(command):
    async def wrapper(client, message):
        try:
            await message.delete()
        except:
            pass

        audio_telegram = (
            (message.reply_to_message.audio or message.reply_to_message.voice)
            if message.reply_to_message else None)
        
        video_telegram = (
            (message.reply_to_message.video or message.reply_to_message.document)
            if message.reply_to_message else None)
        
        url = await YouTubeAPI.url(message)
        
        if audio_telegram is None and video_telegram is None and url is None:
            if len(message.command) < 2:
                if "stream" in message.command:
                    return await message.reply_text("ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴍ3ᴜ8 ᴏʀ ɪɴᴅᴇx ʟɪɴᴋs")
                buttons = botplaylist_markup()
                return await message.reply_photo(
                    photo=BIKASH_IMG,
                    caption="<b><u>ᴜsᴀɢᴇ :</u></b> /play & /bgt [sᴏɴɢ ɴᴀᴍᴇ/ʏᴏᴜᴛᴜʙᴇ ᴜʀʟ/ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴀᴜᴅɪᴏ/ᴠɪᴅᴇᴏ ғɪʟᴇ]",
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
                
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await message.reply_text("» ᴘʟᴇᴀsᴇ ᴅᴇғɪɴᴇ ᴄʜᴀɴɴᴇʟ ɪᴅ ᴠɪᴀ /channelplay")
            try:
                chat = await app.get_chat(chat_id)
            except:
                return await message.reply_text("» ғᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ᴄʜᴀɴɴᴇʟ.\n\nᴍᴀᴋᴇ sᴜʀᴇ ʏᴏᴜ'ᴠᴇ ᴀᴅᴅᴇᴅ ᴛʜᴇ ʙᴏᴛ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴘʀᴏᴍᴏᴛᴇᴅ ᴀs ᴀᴅᴍɪɴ")
            channel = chat.title
        else:
            chat_id = message.chat.id
            channel = None
        playmode = await get_playmode(message.chat.id)
        playty = await get_playtype(message.chat.id)
    
        if playty != "Everyone":
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.chat.id)
                if not admins:
                    return
                else:
                    if message.from_user.id not in admins:
                        return await message.reply_text("<b>ᴀᴅᴍɪɴs ᴏɴʟʏ ᴘʟᴀʏ</b>\nᴏɴʟʏ ᴀᴅᴍɪɴs ᴏғ ᴛʜɪs ᴄʜᴀᴛ ᴀʀᴇ ᴀʟʟᴏᴡᴇᴅ ᴛᴏ ᴘʟᴀʏ\n\nᴄʜᴀɴɢᴇ ᴘʟᴀʏ ᴍᴏᴅᴇ ᴠɪᴀ /playmode") 
                    
        if message.command[0][0] == "v":
            video = True
        else:
            if "-v" in message.text:
                video = True
            else:
                video = True if message.command[0][1] == "v" else None
                
        if message.command[0][-1] == "e":
            if not await is_active_chat(chat_id):
                return await message.reply_text("**Nᴏ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ**")
            fplay = True
        else:
            fplay = None

        if not await is_active_chat(chat_id):
            userbot = await get_assistant(chat_id)
            try:
                try:
                    get = await app.get_chat_member(chat_id, userbot.id)
                except ChatAdminRequired:
                    return await message.reply_text("» ʙᴏᴛ ʀᴇǫᴜɪʀᴇs <b>ɪɴᴠɪᴛᴇ ᴜsᴇʀs ᴠɪᴀ ʟɪɴᴋ</b> ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ɪɴᴠɪᴛᴇ ᴀssɪsᴛᴀɴᴛ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ")
                if (get.status == ChatMemberStatus.BANNED or get.status == ChatMemberStatus.RESTRICTED):
                    try:
                        await app.unban_chat_member(chat_id, userbot.id)
                    except:
                        return await message.reply_text("<b><u>{0} ᴀssɪsᴛᴀɴᴛ ɪs ʙᴀɴɴᴇᴅ</u></b>\n\n<b>ɪᴅ :</b> <code>{1}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{2}\n\nᴘʟᴇᴀsᴇ ᴜɴʙᴀɴ ᴛʜᴇ ᴀssɪsᴛᴀɴᴛ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.".format(app.mention, userbot.id, userbot.username))
            except UserNotParticipant:
                if chat_id in links:
                    invitelink = links[chat_id]
                else:
                    if message.chat.username:
                        invitelink = message.chat.username
                        try:
                            await userbot.resolve_peer(invitelink)
                        except:
                            pass
                    else:
                        try:
                            invitelink = await app.export_chat_invite_link(chat_id)
                        except ChatAdminRequired:
                            return await message.reply_text("» ʙᴏᴛ ʀᴇǫᴜɪʀᴇs <b>ɪɴᴠɪᴛᴇ ᴜsᴇʀs ᴠɪᴀ ʟɪɴᴋ</b> ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ɪɴᴠɪᴛᴇ ᴀssɪsᴛᴀɴᴛ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ.")
                        except Exception as e:
                            return await message.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ɪɴᴠɪᴛᴇ {0}\n\nʀᴇᴀsᴏɴ : <code>{1}</code>".format(app.mention, type(e).__name__))

                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                try:
                    await asyncio.sleep(0.001)
                    await userbot.join_chat(invitelink)
                except InviteRequestSent:
                    try:
                        await app.approve_chat_join_request(chat_id, userbot.id)
                    except Exception as e:
                        return await message.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ɪɴᴠɪᴛᴇ {0}\n\nʀᴇᴀsᴏɴ : <code>{1}</code>".format(app.mention, type(e).__name__))
                    await asyncio.sleep(0.001)
                    await message.reply_text("{0} ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ".format(app.mention))
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    return await message.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ɪɴᴠɪᴛᴇ {0} \n\nʀᴇᴀsᴏɴ : <code>{1}</code>".format(app.mention, type(e).__name__))

                links[chat_id] = invitelink
                try:
                    await userbot.resolve_peer(chat_id)
                except:
                    pass
        return await command(client, message, chat_id, video, channel, playmode, url, fplay)
    return wrapper
