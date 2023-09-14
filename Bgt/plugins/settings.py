from config import BANNED_USERS, CLEAN_MINS
from pyrogram import filters
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardMarkup, Message
from Bgt import app
from Bgt.utils.database import (add_nonadmin_chat, cleanmode_off, cleanmode_on, commanddelete_off, commanddelete_on,
            get_aud_bit_name, get_playmode, get_playtype, get_vid_bit_name, is_cleanmode_on, is_commanddelete_on,
            is_nonadmin_chat, remove_nonadmin_chat, save_audio_bitrate, save_video_bitrate, set_playmode, set_playtype)
from Bgt.utils.inline.settings import (audio_quality_markup, playmode_users_markup,
                     setting_markup, video_quality_markup, cleanmode_settings_markup)
from Bgt.utils.decorators import ActualAdminCB, AdminRightsCheck



@app.on_message(filters.command(["settings", "setting"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def settings_mar(client, message: Message):
    try:
        await message.delete()
    except:
        pass
    buttons = setting_markup()
    await message.reply_text(
        "⚙️ **ᴍᴜsɪᴄ ʙᴏᴛ sᴇᴛᴛɪɴɢs**\n\n🖇 **ɢʀᴏᴜᴘ:** {0}\n🔖 **ɢʀᴏᴜᴘ ɪᴅ:** `{1}`\n\n🌸 **ᴄʜᴏᴏsᴇ ᴛʜᴇ ғᴜɴᴄᴛɪᴏɴ ʙᴜᴛᴛᴏɴs ғʀᴏᴍ ʙᴇʟᴏᴡ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴇᴅɪᴛ ᴏʀ ᴄʜᴀɴɢᴇ**".format(message.chat.title, message.chat.id),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex(r"settings_helper") & ~BANNED_USERS)
async def settings_cb(client, CallbackQuery):
    try:
        await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ʙᴀᴄᴋ ")
    except:
        pass
    buttons = setting_markup()
    return await CallbackQuery.edit_message_text(
        "⚙️ **ᴍᴜsɪᴄ ʙᴏᴛ sᴇᴛᴛɪɴɢs**\n\n🖇 **ɢʀᴏᴜᴘ:** {0}\n🔖 **ɢʀᴏᴜᴘ ɪᴅ:** `{1}`\n\n🌸 **ᴄʜᴏᴏsᴇ ᴛʜᴇ ғᴜɴᴄᴛɪᴏɴ ʙᴜᴛᴛᴏɴs ғʀᴏᴍ ʙᴇʟᴏᴡ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴇᴅɪᴛ ᴏʀ ᴄʜᴀɴɢᴇ**".format(CallbackQuery.message.chat.title, CallbackQuery.message.chat.id),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def gen_buttons_aud(aud):
    if aud == "High":
        buttons = audio_quality_markup(high=True)
    elif aud == "Medium":
        buttons = audio_quality_markup(medium=True)
    elif aud == "Low":
        buttons = audio_quality_markup(low=True)
    return buttons


async def gen_buttons_vid(aud):
    if aud == "High":
        buttons = video_quality_markup(high=True)
    elif aud == "Medium":
        buttons = video_quality_markup(medium=True)
    elif aud == "Low":
        buttons = video_quality_markup(low=True)
    return buttons


@app.on_callback_query(filters.regex(pattern=r"^(SEARCHANSWER|PLAYMODEANSWER|PLAYTYPEANSWER|AUTHANSWER|CMANSWER|COMMANDANSWER|CM|AQ|VQ|PM|)$") & ~BANNED_USERS)
async def without_Admin_rights(client, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    if command == "SEARCHANSWER":
        try:
            return await CallbackQuery.answer("1) ᴅɪʀᴇᴄᴛ: ᴘʟᴀʏs sᴇᴀʀᴄʜ ǫᴜᴇʀɪᴇs ᴅɪʀᴇᴄᴛʟʏ. ᴜsᴇ -ᴠ ᴛᴏ ᴘʟᴀʏ ᴠɪᴅᴇᴏs ɪɴ ᴅɪʀᴇᴄᴛ ᴍᴏᴅᴇ.\n\n2) ɪɴʟɪɴᴇ: ʀᴇᴛᴜʀɴs ɪɴʟɪɴᴇ ᴍᴀʀᴋᴜᴘ ʙᴜᴛᴛᴏɴs ꜰᴏʀ ᴄʜᴏᴏsɪɴɢ ʙᴇᴛᴡᴇᴇɴ ᴠɪᴅᴇᴏ & ᴀᴜᴅɪᴏ.", show_alert=True)
        except:
            return
    elif command == "PLAYMODEANSWER":
        try:
            return await CallbackQuery.answer("1) ɢʀᴏᴜᴘ: ᴘʟᴀʏs ᴍᴜsɪᴄ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ ᴡʜᴇʀᴇ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ɪs ɢɪᴠᴇɴ.\n\n2) ᴄʜᴀɴɴᴇʟ: ᴘʟᴀʏs ᴍᴜsɪᴄ ɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ʏᴏᴜ ᴡᴀɴᴛ. sᴇᴛ ᴄʜᴀɴɴᴇʟ ɪᴅ ᴠɪᴀ /channelplay", show_alert=True)
        except:
            return
    elif command == "PLAYTYPEANSWER":
        try:
            return await CallbackQuery.answer("1) ᴇᴠᴇʀʏᴏɴᴇ: ᴀɴʏᴏɴᴇ ᴘʀᴇsᴇɴᴛ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜsɪᴄ ʜᴇʀᴇ.\n\n2) ᴀᴅᴍɪɴ ᴏɴʟʏ: ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴘʟᴀʏ ᴛʜᴇ ᴍᴜsɪᴄ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.", show_alert=True)
        except:
            return
    elif command == "AUTHANSWER":
        try:
            return await CallbackQuery.answer("👥 ᴇᴠᴇʀʏᴏɴᴇ: ᴀɴʏᴏɴᴇ ᴄᴀɴ ᴜsᴇ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs(sᴋɪᴘ, ᴘᴀᴜsᴇ, ʀᴇsᴜᴍᴇ ᴇᴛᴄ) ᴘʀᴇsᴇɴᴛ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.\n\n🙍 ᴀᴅᴍɪɴ ᴏɴʟʏ: ᴏɴʟʏ ᴀᴅᴍɪɴs ᴀɴᴅ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs ᴄᴀɴ ᴜsᴇ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs.", show_alert=True)
        except:
            return
    elif command == "CMANSWER":
        try:
            return await CallbackQuery.answer("ᴡʜᴇɴ ᴀᴄᴛɪᴠᴀᴛᴇᴅ, ʙᴏᴛ ᴡɪʟʟ ᴅᴇʟᴇᴛᴇ ɪᴛs ᴍᴇssᴀɢᴇ ᴀꜰᴛᴇʀ {0} ᴛᴏ ᴍᴀᴋᴇ ʏᴏᴜʀ ᴄʜᴀᴛ ᴄʟᴇᴀɴ ᴀɴᴅ ᴄʟᴇᴀʀ.".format(CLEAN_MINS), show_alert=True)
        except:
            return
    elif command == "COMMANDANSWER":
        try:
            return await CallbackQuery.answer("ᴡʜᴇɴ ᴀᴄᴛɪᴠᴀᴛᴇᴅ, ʙᴏᴛ ᴡɪʟʟ ᴅᴇʟᴇᴛᴇ ɪᴛs ᴇxᴇᴄᴜᴛᴇᴅ ᴄᴏᴍᴍᴀɴᴅs (/play, /pause, /shuffle, /stop ᴇᴛᴄ) ɪᴍᴍᴇᴅɪᴀᴛᴇʟʏ.\n\nʙᴏᴛ ᴡɪʟʟ ʙᴇ ʀᴇǫᴜɪʀɪɴɢ ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs ᴀᴅᴍɪɴ ʀɪɢʜᴛ ꜰᴏʀ ᴛʜɪs ᴛᴏ ᴡᴏʀᴋ ᴘʀᴏᴘᴇʀʟʏ.", show_alert=True)
        except:
            return
    elif command == "CM":
        try:
            await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ᴄʟᴇᴀɴ ᴍᴏᴅᴇ ᴘᴀɴᴇʟ ", show_alert=True)
        except:
            pass
        sta = None
        cle = None
        if await is_cleanmode_on(CallbackQuery.message.chat.id):
            cle = True
        if await is_commanddelete_on(CallbackQuery.message.chat.id):
            sta = True
        buttons = cleanmode_settings_markup(status=cle, dels=sta)
    elif command == "AQ":
        try:
            await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ᴀᴜᴅɪᴏ ǫᴜᴀʟɪᴛʏ ᴘᴀɴᴇʟ ", show_alert=True)
        except:
            pass
        aud = await get_aud_bit_name(CallbackQuery.message.chat.id)
        buttons = await gen_buttons_aud(aud)
    elif command == "VQ":
        try:
            await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ᴠɪᴅᴇᴏ ǫᴜᴀʟɪᴛʏ ᴘᴀɴᴇʟ ", show_alert=True)
        except:
            pass
        aud = await get_vid_bit_name(CallbackQuery.message.chat.id)
        buttons = await gen_buttons_vid(aud)
    elif command == "PM":
        try:
            await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ᴘʟᴀʏ ᴍᴏᴅᴇ ᴘᴀɴᴇʟ ", show_alert=True)
        except:
            pass
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        Direct = True if playmode == "Direct" else None
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        Group = None if is_non_admin else True
        playty = await get_playtype(CallbackQuery.message.chat.id)
        Playtype = None if playty == "Everyone" else True
        buttons = playmode_users_markup(Direct, Group, Playtype)
    
    try:
        return await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    except MessageNotModified:
        return


@app.on_callback_query(filters.regex(pattern=r"^(LQA|MQA|HQA|LQV|MQV|HQV)$") & ~BANNED_USERS)
@ActualAdminCB
async def aud_vid_cb(client, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    try:
        await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ᴜᴘ ᴄʜᴀɴɢᴇs ", show_alert=True)
    except:
        pass
    if command == "LQA":
        await save_audio_bitrate(CallbackQuery.message.chat.id, "Low")
        buttons = audio_quality_markup(low=True)
    elif command == "MQA":
        await save_audio_bitrate(CallbackQuery.message.chat.id, "Medium")
        buttons = audio_quality_markup(medium=True)
    elif command == "HQA":
        await save_audio_bitrate(CallbackQuery.message.chat.id, "High")
        buttons = audio_quality_markup(high=True)
    elif command == "LQV":
        await save_video_bitrate(CallbackQuery.message.chat.id, "Low")
        buttons = video_quality_markup(low=True)
    elif command == "MQV":
        await save_video_bitrate(CallbackQuery.message.chat.id, "Medium")
        buttons = video_quality_markup(medium=True)
    elif command == "HQV":
        await save_video_bitrate(CallbackQuery.message.chat.id, "High")
        buttons = video_quality_markup(high=True)
    try:
        return await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    except MessageNotModified:
        return


@app.on_callback_query(filters.regex(pattern=r"^(|MODECHANGE|CHANNELMODECHANGE|PLAYTYPECHANGE)$") & ~BANNED_USERS)
@ActualAdminCB
async def playmode_ans(client, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    if command == "CHANNELMODECHANGE":
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if is_non_admin:
            await remove_nonadmin_chat(CallbackQuery.message.chat.id)
            Group = True
        else:
            await add_nonadmin_chat(CallbackQuery.message.chat.id)
            Group = None
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            Playtype = None
        else:
            Playtype = True
        buttons = playmode_users_markup(Direct, Group, Playtype)
    elif command == "MODECHANGE":
        try:
            await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ᴜᴘ ᴄʜᴀɴɢᴇs ", show_alert=True)
        except:
            pass
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            await set_playmode(CallbackQuery.message.chat.id, "Inline")
            Direct = None
        else:
            await set_playmode(CallbackQuery.message.chat.id, "Direct")
            Direct = True
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if is_non_admin:
            Group = None
        else:
            Group = True
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            Playtype = False
        else:
            Playtype = True
        buttons = playmode_users_markup(Direct, Group, Playtype)
    elif command == "PLAYTYPECHANGE":
        try:
            await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ᴜᴘ ᴄʜᴀɴɢᴇs ", show_alert=True)
        except:
            pass
        playty = await get_playtype(CallbackQuery.message.chat.id)
        if playty == "Everyone":
            await set_playtype(CallbackQuery.message.chat.id, "Admin")
            Playtype = False
        else:
            await set_playtype(CallbackQuery.message.chat.id, "Everyone")
            Playtype = True
        playmode = await get_playmode(CallbackQuery.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if is_non_admin:
            Group = None
        else:
            Group = True
        buttons = playmode_users_markup(Direct, Group, Playtype)
    try:
        return await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    except MessageNotModified:
        return


@app.on_callback_query(filters.regex(pattern=r"^(CLEANMODE|COMMANDELMODE)$") & ~BANNED_USERS)
@ActualAdminCB
async def cleanmode_mark(client, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    try:
        await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ᴜᴘ ᴄʜᴀɴɢᴇs ", show_alert=True)
    except:
        pass

    if command == "CLEANMODE":
        sta = None
        if await is_commanddelete_on(CallbackQuery.message.chat.id):
            sta = True
        cle = None
        if await is_cleanmode_on(CallbackQuery.message.chat.id):
            await cleanmode_off(CallbackQuery.message.chat.id)
        else:
            await cleanmode_on(CallbackQuery.message.chat.id)
            cle = True
        buttons = cleanmode_settings_markup(status=cle, dels=sta)
        return await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))

    elif command == "COMMANDELMODE":
        cle = None
        sta = None
        if await is_cleanmode_on(CallbackQuery.message.chat.id):
            cle = True
        if await is_commanddelete_on(CallbackQuery.message.chat.id):
            await commanddelete_off(CallbackQuery.message.chat.id)
        else:
            await commanddelete_on(CallbackQuery.message.chat.id)
            sta = True
        buttons = cleanmode_settings_markup(status=cle, dels=sta)

    try:
        return await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    except MessageNotModified:
        return
