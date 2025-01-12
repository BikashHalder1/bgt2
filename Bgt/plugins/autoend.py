from pyrogram import filters
from Bgt import app
from Bgt.misc import SUDOERS
from Bgt.utils.database import autoend_off, autoend_on


@app.on_message(filters.command(["autoend"]) & SUDOERS)
async def auto_end_stream(c, message):
    try:
        await message.delete()
    except:
        pass
    usage = "**Usage:**\n/autoend [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)

    state = message.text.split(None, 1)[1].strip()
    state = state.lower()

    if state == "enable":
        await autoend_on()
        await message.reply_text("ᴀᴜᴛᴏ ᴇɴᴅ sᴛʀᴇᴀᴍ ᴇɴᴀʙʟᴇᴅ")
    elif state == "disable":
        await autoend_off()
        await message.reply_text("ᴀᴜᴛᴏ ᴇɴᴅ sᴛʀᴇᴀᴍ ᴅɪsᴀʙʟᴇᴅ")
    else:
        await message.reply_text(usage)
