import imghdr
import os
from asyncio import gather
from config import BANNED_USERS
from traceback import format_exc
from pyrogram.errors import PeerIdInvalid, ShortnameOccupyFailed, StickerEmojiInvalid, StickerPngDimensions, StickerPngNopng, UserIsBlocked
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram import filters
from Bgt import app
from Bgt.utils.stickerset import (get_document_from_file_id, resize_file_to_sticker_size, upload_document,
                            add_sticker_to_set, create_sticker, create_sticker_set, get_sticker_set_by_name)


__MODULE__ = "Sᴛɪᴄᴋᴇʀ"
__HELP__ = """    
⊱ /kang - ᴛᴏ ᴋᴀɴɢ ᴀ sᴛɪᴄᴋᴇʀ ᴏʀ ᴀɴ ɪᴍᴀɢᴇ

⊱ /stickerid - ᴛᴏ ɢᴇᴛ ғɪʟᴇ ɪᴅ ᴏғ ᴀ sᴛɪᴄᴋᴇʀ

⊱ /getsticker - ᴛᴏ ɢᴇᴛ sᴛɪᴄᴋᴇʀ ᴀs ᴀ ᴘʜᴏᴛᴏ ᴀɴᴅ ᴅᴏᴄᴜᴍᴇɴᴛ
"""


MAX_STICKERS = 120  

SUPPORTED_TYPES = ["jpeg", "png", "webp"]


def kang_panel():
    buttons = InlineKeyboardMarkup(
        [
          [
            InlineKeyboardButton(text="Start", url=f"https://t.me/{app.username}?start")
          ]
        ]
    )
    return buttons


@app.on_message(filters.command("stickerid") & ~BANNED_USERS)
async def sticker_id(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    reply = message.reply_to_message
    if not reply:
        return await message.reply("ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ... ✨")
    if not reply.sticker:
        return await message.reply("ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ... ✨")
    await message.reply_text(f"`{reply.sticker.file_id}`")


@app.on_message(filters.command("getsticker") & ~BANNED_USERS)
async def sticker_image(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    r = message.reply_to_message
    if not r:
        return await message.reply("ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ... ✨")
    if not r.sticker:
        return await message.reply("ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ... ✨")
    m = await message.reply("`sᴇɴᴅɪɴɢ ...`")
    f = await r.download(f"{r.sticker.file_unique_id}.png")
    await gather(
        *[
            message.reply_photo(f),
            message.reply_document(f),
        ]
    )
    await m.delete()
    os.remove(f)


@app.on_message(filters.command("kang") & ~BANNED_USERS)
async def kang(client, message: Message):
    try:
        await message.delete()
    except:
        pass
    if not message.reply_to_message:
        return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ/ɪᴍᴀɢᴇ ᴛᴏ ᴋᴀɴɢ ɪᴛ !")
    if not message.from_user:
        return await message.reply_text("ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴ ᴀᴅᴍɪɴ ᴋᴀɴɢ sᴛɪᴄᴋᴇʀs ɪɴ ᴍʏ ᴘᴍ !")
    msg = await message.reply_text("ᴋᴀɴɢɪɴɢ sᴛɪᴄᴋᴇʀ !")

    args = message.text.split()
    if len(args) > 1:
        sticker_emoji = str(args[1])
    elif message.reply_to_message.sticker and message.reply_to_message.sticker.emoji:
        sticker_emoji = message.reply_to_message.sticker.emoji
    else:
        sticker_emoji = "🥀"

    doc = message.reply_to_message.photo or message.reply_to_message.document
    try:
        if message.reply_to_message.sticker:
            sticker = await create_sticker(
                await get_document_from_file_id(message.reply_to_message.sticker.file_id),
                sticker_emoji,
            )
        elif doc:
            if doc.file_size > 10000000:
                return await msg.edit("File size too large !")

            temp_file_path = await app.download_media(doc)
            image_type = imghdr.what(temp_file_path)
            if image_type not in SUPPORTED_TYPES:
                return await msg.edit("ғᴏʀᴍᴀᴛ ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ ! ({})".format(image_type))
            try:
                temp_file_path = await resize_file_to_sticker_size(temp_file_path)
            except OSError as e:
                await msg.edit_text("sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ !")
                raise Exception(f"sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ᴡʜɪʟᴇ ʀᴇsɪᴢɪɴɢ ᴛʜᴇ sᴛɪᴄᴋᴇʀ (at {temp_file_path}); {e}")
            sticker = await create_sticker(
                await upload_document(client, temp_file_path, message.chat.id),
                sticker_emoji,
            )
            if os.path.isfile(temp_file_path):
                os.remove(temp_file_path)
        else:
            return await msg.edit("ɴᴏᴘᴇ ᴄᴀɴ'ᴛ ᴋᴀɴɢ ᴛʜᴀᴛ !")
    except ShortnameOccupyFailed:
        await message.reply_text("ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ɴᴀᴍᴇ ᴏʀ ᴜsᴇʀɴᴀᴍᴇ !")
        return

    except Exception as e:
        await message.reply_text(str(e))
        e = format_exc()
        return print(e)

    packnum = 0
    packname = "f" + str(message.from_user.id) + "_by_" + app.username
    limit = 0
    try:
        while True:
            if limit >= 50:
                return await msg.delete()

            stickerset = await get_sticker_set_by_name(client, packname)
            if not stickerset:
                stickerset = await create_sticker_set(
                    client,
                    message.from_user.id,
                    f"{message.from_user.first_name[:32]}'s Pᴀᴄᴋ",
                    packname,
                    [sticker],
                )
            elif stickerset.set.count >= MAX_STICKERS:
                packnum += 1
                packname = (
                    "f"
                    + str(packnum)
                    + "_"
                    + str(message.from_user.id)
                    + "_by_"
                    + app.username
                )
                limit += 1
                continue
            else:
                try:
                    await add_sticker_to_set(client, stickerset, sticker)
                except StickerEmojiInvalid:
                    return await msg.edit("[ERROR]: INVALID_EMOJI_IN_ARGUMENT")
            limit += 1
            break
        
        buttons = InlineKeyboardMarkup(
            [
              [
                InlineKeyboardButton(text="Your Pack", url=f"t.me/addstickers/{packname}")
              ]
            ]
        )
        await msg.edit("Sticker Kanged To Your [Pack](t.me/addstickers/{})\nEmoji: {}".format(packname, sticker_emoji), reply_markup=buttons)
    except (PeerIdInvalid, UserIsBlocked):
        keyboard = kang_panel()
        await msg.edit("You Need To Start A Private Chat With Me !", reply_markup=keyboard)
    except StickerPngNopng:
        await message.reply_text("Stickers must be png files but the provided image was not a png !")
    except StickerPngDimensions:
        await message.reply_text("The sticker png dimensions are invalid !")
