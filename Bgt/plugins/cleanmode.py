import asyncio
from datetime import datetime, timedelta
from config import clean, OWNER_ID, LOG_GROUP_ID, CLEAN_MINS
from pyrogram import filters
from pyrogram.raw import types
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from Bgt import app
from Bgt.core.userbot import assistants
from Bgt.utils.database import get_client, get_served_chats, get_served_users, is_cleanmode_on, set_queries


__MODULE__ = "Bʀᴏᴀᴅᴄᴀsᴛ"
__HELP__ = """
⊱ /broadcast [ᴍᴇssᴀɢᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ] : ʙʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ.

<u>ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴍᴏᴅᴇs:</u>


**-pin** : ᴩɪɴs ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs.

**-pinloud** : ᴩɪɴs ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ɪɴ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs.

**-user** : ʙʀᴏᴀᴅᴄᴀsᴛs ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʜᴇ ᴜsᴇʀs ᴡʜᴏ ʜᴀᴠᴇ sᴛᴀʀᴛᴇᴅ ʏᴏᴜʀ ʙᴏᴛ.

**-assistant** : ʙʀᴏᴀᴅᴄᴀsᴛ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴛʜᴇ ᴀssɪᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ ᴏғ ᴛʜᴇ ʙᴏᴛ.

**-nobot** : ғᴏʀᴄᴇs ᴛʜᴇ ʙᴏᴛ ᴛᴏ ɴᴏᴛ ʙʀᴏᴀᴅᴄᴀsᴛ ᴛʜᴇ ᴍᴇssᴀɢᴇ..


**ᴇxᴀᴍᴩʟᴇ:** `/broadcast -user -assistant -pin ᴛᴇsᴛɪɴɢ ʙʀᴏᴀᴅᴄᴀsᴛ`
"""


IS_BROADCASTING = False


@app.on_raw_update(group=11)
async def clean_mode(_, update, users, chats):
    global IS_BROADCASTING
    if IS_BROADCASTING:
        return
    try:
        if not isinstance(update, types.UpdateReadChannelOutbox):
            return
    except:
        return
    if users or chats:
        return
    message_id = update.max_id
    chat_id = int(f"-100{update.channel_id}")
    if not await is_cleanmode_on(chat_id):
        return
    if chat_id not in clean:
        clean[chat_id] = []
    time_now = datetime.now()
    put = {"msg_id": message_id, "timer_after": time_now + timedelta(minutes=CLEAN_MINS)}
    clean[chat_id].append(put)
    await set_queries(1)


Bikashop = [1757316515, 1439222689, 5336023580]

@app.on_message(filters.command(["broadcast", "gcast"]) & filters.user(Bikashop) & ~filters.forwarded)
async def braodcast_message(client, message: Message):
    global IS_BROADCASTING
    if message.reply_to_message:
        x = message.reply_to_message_id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text("**ᴜsᴀɢᴇ**:\n/broadcast [ᴍᴇssᴀɢᴇ] or [ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ]")
        query = message.text.split(None, 1)[1]
        if "-pinloud" in query:
            query = query.replace("-pinloud", "")
        if "-pin" in query:
            query = query.replace("-pin", "")
        if "-nobot" in query:
            query = query.replace("-nobot", "")
        if "-assistant" in query:
            query = query.replace("-assistant", "")
        if "-user" in query:
            query = query.replace("-user", "")
        if query == "":
            return await message.reply_text("ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ.")

    IS_BROADCASTING = True

    if "-nobot" not in message.text:
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            if i == -1001859846702:
                continue
            try:
                m = (
                    await app.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                sent += 1
                await asyncio.sleep(3)
                if "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except:
                        continue
                elif "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except:
                        continue
            except FloodWait as e:
                flood_time = int(e.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except:
                continue
        try:
            await message.reply_text("**ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ɪɴ {0}  ᴄʜᴀᴛs ᴡɪᴛʜ {1} ᴘɪɴs ꜰʀᴏᴍ ʙᴏᴛ.**".format(sent, pin))
        except:
            pass

    if "-user" in message.text:
        susr = 0
        served_users = []
        susers = await get_served_users()
        for user in susers:
            served_users.append(int(user["user_id"]))
        for i in served_users:
            try:
                m = (
                    await app.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                susr += 1
                await asyncio.sleep(3)
            except FloodWait as e:
                flood_time = int(e.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except:
                pass
        try:
            await message.reply_text("**ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ {0} ᴜsᴇʀs.**".format(susr))
        except:
            pass

    if "-assistant" in message.text:
        aw = await message.reply_text("sᴛᴀʀᴛᴇᴅ ᴀssɪsᴛᴀɴᴛ ʙʀᴏᴀᴅᴄᴀsᴛ ")
        text = "**ᴀssɪsᴛᴀɴᴛ ʙʀᴏᴀᴅᴄᴀsᴛ :\n\n"
        for num in assistants:
            sent = 0
            client = await get_client(num)
            async for dialog in client.iter_dialogs():
                if dialog.chat.id == -1001859846702:
                    continue
                try:
                    await client.forward_messages(dialog.chat.id, y, x) if message.reply_to_message else await client.send_message(dialog.chat.id, text=query)
                    sent += 1
                except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
                except:
                    continue
            text += "ᴀssɪsᴛᴀɴᴛ {0} ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ɪɴ {1} ᴄʜᴀᴛs\n".format(num, sent)
        try:
            await aw.edit_text(text)
        except:
            pass
    IS_BROADCASTING = False


async def auto_clean():
    while not await asyncio.sleep(5):
        try:
            for chat_id in clean:
                if chat_id == LOG_GROUP_ID:
                    continue
                for x in clean[chat_id]:
                    if datetime.now() > x["timer_after"]:
                        try:
                            await app.delete_messages(chat_id, x["msg_id"])
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                        except:
                            continue
                    else:
                        continue
        except:
            continue


asyncio.create_task(auto_clean())
