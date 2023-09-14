import os, random, glob
import numpy as np
from config import LOG_GROUP_ID, BANNED_USERS
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatMemberUpdated
from pyrogram.enums import ParseMode, ChatMemberStatus, ChatType
from pyrogram.errors import MessageIdInvalid
from Bgt import app
from Bgt.utils.database import add_served_chat, blacklisted_chats, get_assistant
from Bgt.utils.inline import start_pannel, close_keyboard


def thumbnail(userimg, background, welcomemsg, userinfo):
    try:
        def create_thumbnail(userimg):
            x = Image.open(userimg)
            x.thumbnail((300, 300))
            x.save("thumbnail.jpg")
            thumb = Image.open("thumbnail.jpg")
            constrast = ImageEnhance.Contrast(thumb)
            thumb = constrast.enhance(1.5)
            draw = ImageDraw.Draw(thumb)
            height, width = thumb.size
            lum_img = Image.new("L", thumb.size, 0)
            draw = ImageDraw.Draw(lum_img)
            draw.pieslice([(0, 0), (height, width)], 0, 360, fill=255, outline="white")

            img_arr = np.array(thumb)
            lum_img_arr = np.array(lum_img)
            final_img_arr = np.dstack((img_arr, lum_img_arr))
            thumbn = Image.fromarray(final_img_arr)
            return thumbn

        y = create_thumbnail(userimg)
        bg = Image.open(background)
        bg = bg.filter(ImageFilter.BoxBlur(8))
        combine = bg.copy()
        combine.paste(y, (500, 150), mask=y)
        combine.save("ok.png")


        def add_text_to_image():
            img = Image.open("ok.png")
            d1 = ImageDraw.Draw(img)
            font = "Bgt/assets/BebasNeue.otf"
            my_font = ImageFont.truetype(font, size=80)
            my_font2 = ImageFont.truetype(font, size=35)
            
            d1.line((300, 570, 1000, 570), fill="white", width=4)
            d1.text((300, 50), welcomemsg, font=my_font, fill=(224, 224, 224), stroke_width=1, stroke_fill="#f50727")
            d1.multiline_text((500, 580), userinfo, font=my_font2, fill=(224, 224, 224), stroke_width=1, stroke_fill="#f50727")
     
            im1 = img.crop((0, 0, 1280, 720))
            im1.save("final.jpg")

        add_text_to_image()
        
    except Exception as e:
        print(e)


def wel_panel():
    buttons = [
        [
            InlineKeyboardButton(text="➕ Aᴅᴅ Mᴇ ➕", url=f"https://t.me/{app.username}?startgroup=new")
        ],
        [
            InlineKeyboardButton(text="Gʀᴏᴜᴘ Rᴜʟᴇs", url=f"https://t.me/{app.username}?start=rule")
        ]
    ]
    return buttons


@app.on_message(filters.new_chat_members & ~BANNED_USERS, group=13)
async def welcome_bgt(c, message: Message):
    chat_id = message.chat.id
    await add_served_chat(chat_id)
    if app.id in [user.id for user in message.new_chat_members]:
        if chat_id in await blacklisted_chats():
            await message.reply_text("**ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛ**\n\nᴛʜɪs ᴄʜᴀᴛ ɪs ʙʟᴀᴄᴋʟɪsᴛ ғᴏʀ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ. ʀᴇǫᴜᴇsᴛ ᴀ sᴜᴅᴏ ᴜsᴇʀ ᴛᴏ ᴡʜɪᴛᴇʟɪsᴛ ʏᴏᴜʀ ᴄʜᴀᴛ sᴜᴅᴏ ᴜsᴇʀs [ʟɪsᴛ]({0}).".format(f"https://t.me/{app.username}?start=sudolist"))
            return await app.leave_chat(chat_id)
        userbot = await get_assistant(message.chat.id)
        out = start_pannel()
        await message.reply_text(
            "Hᴇʏ ᴛʜɪs ɪs {0}\nᴀ ғᴀsᴛ ᴀɴᴅ ᴩᴏᴡᴇʀғᴜʟ ᴍᴜsɪᴄ ᴩʟᴀʏᴇʀ ʙᴏᴛ ᴡɪᴛʜ sᴏᴍᴇ ᴀᴡᴇsᴏᴍᴇ ғᴇᴀᴛᴜʀᴇs\n\n๏ ᴀssɪsᴛᴀɴᴛ ᴜsᴇʀɴᴀᴍᴇ :- @{1}\n๏ ᴀssɪsᴛᴀɴᴛ ɪᴅ :- {2}".format(app.mention, userbot.username, userbot.id),
            reply_markup=InlineKeyboardMarkup(out),
        )
        add_m = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
        add_id = message.from_user.username if message.from_user else "None"
        title = message.chat.title
        uname = f"@{message.chat.username}" if message.chat.username else "ᴩʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
        chat_id = message.chat.id
        new = f"**✫** <b><u>ɴᴇᴡ ɢʀᴏᴜᴘ</u></b> **:**\n\n**ᴄʜᴀᴛ ɪᴅ :** {chat_id}\n**ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :** {uname}\n**ᴄʜᴀᴛ Tɪᴛʟᴇ :** {title}\n\n**ᴀᴅᴅᴇᴅ ʙʏ :** {add_m}\n**ᴀᴅᴅᴇᴅ ʙʏ :** @{add_id}"
        chat = await app.get_chat(chat_id)
        try:
            link = chat.invite_link
            if not link:
                link = await app.export_chat_invite_link(chat_id)
        except:
            return
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Group Link", url=f"{link}")]
            ]
        )
        await app.send_message(LOG_GROUP_ID, new, reply_markup=keyboard)
            

@app.on_message(~filters.me & ~filters.forwarded & ~BANNED_USERS, group=14)
async def watcher(c, m: Message):
    text = m.text
    if m.chat.type == ChatType.PRIVATE:
        try:
            if text.startswith("/start"):
                return
            if text:
                await c.forward_messages(LOG_GROUP_ID, m.chat.id, m.id)
            else:
                return
        except AttributeError:
            pass
        except MessageIdInvalid:
            pass
    else:
        return
          
        
@app.on_chat_member_updated(filters.group & ~BANNED_USERS, group=15)
async def member_has_joined(c: app, member: ChatMemberUpdated):
    back_img = random.choice(glob.glob("Bgt/assets/background*"))
    if (
        member.new_chat_member
        and not member.old_chat_member
        and not member.new_chat_member.user.is_bot == "true"
        and member.new_chat_member.user.status
        not in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]
    ):
        pass
    else:
        return
    
    user = member.new_chat_member.user if member.new_chat_member else member.from_user
    user_photo = user.photo.big_file_id if user.photo else None
    username = "@" + user.username if user.username else "None"
    fullname = user.first_name + user.last_name if user.last_name else  user.first_name
    IMGX = wel_panel()
    info = f"Username  :  {username}\n\nUser id  :  {user.id}"
    
    if not user_photo:
        thumbnail("Bgt/assets/randompic.jpg", back_img, welcomemsg=f"welcome in this group", userinfo=info)
        return await c.send_photo(
            member.chat.id,
            photo="final.jpg",
            caption=f"""<b><u>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {member.chat.title} </u><br>
            
ɴᴀᴍᴇ : {fullname}
ᴜꜱᴇʀ ɪᴅ : <code>{user.id}</code>
ᴜꜱᴇʀɴᴀᴍᴇ : {username}
ᴍᴇɴᴛɪᴏɴ : {user.mention}
ᴊᴏɪɴᴇᴅ ᴀᴛ: {member.date} </b>""",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(IMGX),
        )

    userphoto = await c.download_media(user.photo.big_file_id)
    thumbnail(userphoto, back_img, welcomemsg=f"welcome in this group", userinfo=info)
    await c.send_photo(
        member.chat.id,
        photo="final.jpg",
        caption=f"""<b><u>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {member.chat.title} </u><br>
        
ɴᴀᴍᴇ : {fullname}
ᴜꜱᴇʀ ɪᴅ : <code>{user.id}</code>
ᴜꜱᴇʀɴᴀᴍᴇ : {username} 
ᴍᴇɴᴛɪᴏɴ : {user.mention}
ᴊᴏɪɴᴇᴅ ᴀᴛ: {member.date} </b>""",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(IMGX),
    )
    try:
        os.remove("ok.png")
        os.remove(userphoto)
        os.remove("final.jpg")
        os.remove("thumbnail.jpg")
    except FileNotFoundError:
        pass
