import pyfiglet 
from config import BANNED_USERS
from random import choice
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from Bgt import app


__MODULE__ = "Fɪɢʟᴇᴛ"
__HELP__ = f""" 
⊱ ᴍᴀᴋᴇs ғɪɢʟᴇᴛ ᴏғ ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ
 
ᴇx : `/figlet Bgt`
"""

def figle(text):
    x = pyfiglet.FigletFont.getFonts()
    font = choice(x)
    figled = str(pyfiglet.figlet_format(text, font=font))
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ᴄʜᴀɴɢᴇ", callback_data="figlet"),
                InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
            ]
        ]
    )
    return figled, keyboard


@app.on_message(filters.command("figlet") & ~BANNED_USERS)
async def echo_figlet(bot, message):
    try:
        await message.delete()
    except:
        pass
    global text
    try:
        text = message.text.split(' ',1)[1]
    except IndexError:
        return await message.reply_text("Example:\n\n`/figlet Bgt`")
    kul_text, keyboard = figle(text)
    try:
        await message.reply_text(f"ʜᴇʀᴇ ɪs ʏᴏᴜʀ ғɪɢʟᴇᴛ :\n<pre>{kul_text}</pre>", quote=True, reply_markup=keyboard)
    except:
        return
    

@app.on_callback_query(filters.regex("figlet"))
async def figlet_handler(bot, query: CallbackQuery):
  try:
      kul_text, keyboard = figle(text)
      await query.message.edit_text(f"ʜᴇʀᴇ ɪs ʏᴏᴜʀ ғɪɢʟᴇᴛ :\n<pre>{kul_text}</pre>", reply_markup=keyboard)
  except Exception as e : 
      await query.message.reply(e)
      
      
