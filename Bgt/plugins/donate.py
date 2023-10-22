from pyrogram import filters

from Bgt import app

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


@app.on_message(
    filters.command("donate")
async def donate(bot: app, message: Message):
    await message.reply_photo(
        photo=f"https://te.legra.ph/file/f73af9a4ffe130a83d8d2.jpg",
        caption=f"""ɪғ Yᴏᴜ ᴡᴀɴɴᴀ ᴅᴏɴᴀᴛᴇ ғᴏʀ ᴏᴜʀ ᴡᴏʀᴋ ᴛʜᴇɴ ᴜsᴇ ᴛʜɪs ᴜᴘɪ ɪᴅ ɢᴘᴀʏ ᴜᴘɪ ɪᴅ : `smartboy8391@okicici` ᴅᴏɴᴀᴛᴇ ᴜsɪɴɢ ᴀɴʏ ᴘᴀʏᴍᴇɴᴛ ᴀᴘᴘ ( ᴏɴʟʏ ғᴏʀ ɪɴᴅɪᴀɴ ) ғᴏʀ ǫʀ & ᴏᴛʜᴇʀs ᴄᴏᴜɴᴛʀʏ ᴘᴀʏᴍᴇɴᴛ ᴍᴇᴛʜᴏᴅ❗ ᴄᴏɴᴛᴀᴄᴛ ғᴏʀ ᴘᴀɪᴅ ᴘʀᴏᴍᴏᴛɪᴏɴ [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://t.me/BgtPromote) Sᴜʙᴄʀɪʙᴇ ᴏᴜʀ [Yᴏᴜᴛᴜʙᴇ Cʜᴀɴɴᴇʟ](https://youtube.com/@bikashgadgetstech)..""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🥀 ʙɪᴋᴀsʜ 🥀", url=f"https://t.me/BikashHalder")
            ],          
            [
                    InlineKeyboardButton(
                        "🥀 ᴅᴘ 🥀", url=f"https://t.me/bikashdp")
                ],
                [
                    InlineKeyboardButton(
                        "🥀 sᴜᴘᴘᴏʀᴛ 🥀", url=f"https://t.me/Bgt_Chat"
                    ),
                    InlineKeyboardButton(
                        "🥀 ᴜᴘᴅᴀᴛᴇs 🥀", url=f"https://t.me/BikashGadgetsTech")
                ]
            ]
        ),
    )