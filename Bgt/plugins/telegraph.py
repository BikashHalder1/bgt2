import os

from Bgt import app

from pyrogram import *
from pyrogram.types import *
from telegraph import Telegraph, upload_file


telegraph = Telegraph()
filesize = 5242880 #[5MB]


@app.on_message(filters.command("tl", "tgm", "tlink"))
async def telegraph_uploader(app, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    replied = message.reply_to_message
    m = await message.reply_text("<b>🔄 Pʀᴏᴄᴇssɪɴɢ ✨...</b>")
    if replied:
        text_msg = replied.text
        animates = replied.animation
        media = (replied.animation or replied.photo
              or replied.video or replied.document)
        sticker =  replied.sticker
    else:
        return await m.edit(f"**⚠️ Pʟᴇᴀsᴇ Rᴇᴘʟʏ Tᴏ A Mᴇᴅɪᴀ\nOʀ Tᴇxᴛ Tᴏ Gᴇɴᴇʀᴀᴛᴇ\nTᴇʟᴇɢʀᴀᴘʜ Lɪɴᴋ❗...**")
    try:
        if text_msg:
            telegraph.create_account(short_name=f"{message.from_user.first_name}")
            author_name = str(message.from_user.first_name)
            author_url = f"https://t.me/{message.from_user.username}" if message.from_user.username else "https://t.me/BikashGadgetsTech"
            if len(message.command) > 1:
                text_title = ' '.join(message.command[1:])
            else:
                text_title = str(message.from_user.first_name + " " + (message.from_user.last_name or ""))
            await m.edit("<b>📤 Uᴘʟᴏᴀᴅɪɴɢ Tᴏ Tᴇʟᴇɢʀᴀᴘʜ</b>")
            response = telegraph.create_page(title=text_title, html_content=text_msg, author_name=author_name, author_url=author_url)
            upload_link = f"https://telegra.ph/{response['path']}"
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🌐 ᴡᴇʙ ᴘʀᴇᴠɪᴇᴡ 🌐", url=upload_link)
                    ]
                ]
            )
            return await m.edit(f"<b>✅ Uᴘʟᴏᴀᴅᴇᴅ Tᴏ Tᴇʟᴇɢʀᴀᴘʜ.</b>\n\n <code>{upload_link}</code>", reply_markup=buttons, disable_web_page_preview=True)
        elif media:
            if media.file_size <= filesize:
                await m.edit("<b>📥 Dᴏᴡɴʟᴏᴀᴅɪɴɢ ✨...</b>")
                local_path = f"./downloads/{user_id}_{media.file_unique_id}/"
                local_file = await replied.download(local_path)
            else:
                return await m.edit("`⚠️ Fɪʟᴇ Sɪᴢᴇ Is Tᴏᴏ Bɪɢ❗...`")
        elif sticker:
            return await m.edit("`🚫 Sᴏʀʀʏ, Sᴛɪᴄᴋᴇʀ Uᴘʟᴏᴀᴅ\nNᴏᴛ Aʟʟᴏᴡᴇᴅ❗...`")
        else:
            return
        await m.edit("<b>📤 Uᴘʟᴏᴀᴅɪɴɢ Tᴏ Tᴇʟᴇɢʀᴀᴘʜ</b>")
        upload_path = upload_file(local_file)
        upload_link = f"https://telegra.ph{upload_path[0]}"
        buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🌐 ᴡᴇʙ ᴘʀᴇᴠɪᴇᴡ 🌐", url=upload_link)
                    ]
                ]
            )
        await m.edit(f"<b>✅ Uᴘʟᴏᴀᴅᴇᴅ Tᴏ Tᴇʟᴇɢʀᴀᴘʜ.</b>\n\n <code>{upload_link}</code>", reply_markup=buttons, disable_web_page_preview=True)
        os.system(f"rm -rf {local_path}")
    except Exception as e:
        await m.edit(f"**🚫 Eʀʀᴏʀ:** `{e}`")
        pass

__MODULE__ = "T-Gʀᴀᴘʜ"
__HELP__ = """
**Tᴇʟᴇɢʀᴀᴘʜ Tᴇxᴛ|Mᴇᴅɪᴀ Uᴘʟᴏᴀᴅᴇʀ**

/tl or /tgm or /tlink - ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴍᴇᴅɪᴀ ᴏʀ ᴛᴇxᴛ ᴛᴏ
ᴜᴘʟᴏᴀᴅ ᴏɴ ᴛᴇʟᴇɢʀᴀᴘʜ.

/tl [title] >> ᴛᴏ sᴇᴛ ᴄᴜsᴛᴏᴍ ᴛɪᴛʟᴇ
ᴏғ ᴛᴇʟᴇɢʀᴀᴘʜ ᴘᴏsᴛ.
"""
