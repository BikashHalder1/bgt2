from math import ceil
from pyrogram.types import InlineKeyboardButton
from config import LOAD, NO_LOAD


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def page_load(page_n, module_dict, prefix, chat=None):
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({})".format(
                        prefix, x.__MODULE__.lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({},{})".format(
                        prefix, chat, x.__MODULE__.lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )

    pairs = list(zip(modules[::3], modules[1::3], modules[2::3]))
    i = 0
    
    for m in pairs:
        for _ in m:
            i += 1
    if len(modules) - i == 1:
        pairs.append((modules[-1],))
    elif len(modules) - i == 2:
        pairs.append(
            (
                modules[-2],
                modules[-1],
            )
        )

    COLUMN_SIZE = 5

    max_num_pages = ceil(len(pairs) / COLUMN_SIZE)
    modulo_page = page_n % max_num_pages

    if len(pairs) > COLUMN_SIZE:
        pairs = pairs[
            modulo_page * COLUMN_SIZE : COLUMN_SIZE * (modulo_page + 1)
        ] + [
            (
                EqInlineKeyboardButton(
                    "◁",
                    callback_data="{}_prev({})".format(prefix, modulo_page),
                ),
                EqInlineKeyboardButton(
                    "Hᴏᴍᴇ",
                    callback_data="semxx",
                ),
                EqInlineKeyboardButton(
                    "▷",
                    callback_data="{}_next({})".format(prefix, modulo_page),
                ),
            ),
        ]
    else:
        pairs = pairs[
            modulo_page * COLUMN_SIZE : COLUMN_SIZE * (modulo_page + 1)
        ] + [
           [
               InlineKeyboardButton(text="Hᴏᴍᴇ", callback_data="semxx")
           ]
        ]

    return pairs


def is_module_loaded(name):
    return (not LOAD or name in LOAD) and name not in NO_LOAD
from sys import version as pyver
from pyrogram import filters, __version__ as pyrover
from config import BANNED_USERS, SUPPORT_HEHE, EXTRA_IMG
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram.enums import ChatType
from Bgt import app, HELPABLE, __Version__
from Bgt.utils.eqline import page_load
from Bgt.utils.inline import private_panel, start_pannel, private_help_panel, setting_markup



@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
async def start_testbot(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    out = start_pannel()
    await message.reply_photo(
        photo=EXTRA_IMG,
        caption=f"🖤 ᴛʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ɪɴ {message.chat.title}.", 
        reply_markup=InlineKeyboardMarkup(out)
    )
    return


@app.on_callback_query(filters.regex(r"setting_back_help") & ~BANNED_USERS)
async def settings_back_markup(_, query: CallbackQuery):
    if query.message.chat.type == ChatType.PRIVATE:
        buttons = private_panel()
        await query.message.edit_caption(
            caption="ʜᴇʏ {0} \nᴛʜɪs ɪs {1} ᴀ ᴛᴇʟᴇɢʀᴀᴍ ꜱᴛʀᴇᴀᴍɪɴɢ ʙᴏᴛ ᴡɪᴛʜ ꜱᴏᴍᴇ ᴀᴡᴇꜱᴏᴍᴇ ꜰᴇᴀᴛᴜʀᴇꜱ.\n\nꜱᴜᴘᴘᴏʀᴛɪɴɢ ᴘʟᴀᴛꜰᴏʀᴍꜱ ʟɪᴋᴇ **ʏᴏᴜᴛᴜʙᴇ**, **ꜱᴘᴏᴛɪꜰʏ** ᴇᴛᴄ.\n\n**ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ɪɴғᴏ ᴀʙᴏᴜᴛ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs.**".format(query.from_user.first_name, app.mention),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        buttons = setting_markup()
        return await query.edit_message_reply_markup(InlineKeyboardMarkup(buttons))

    
@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(_, query: CallbackQuery):
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    
    if mod_match:
        module = mod_match.group(1)
        text = (
            "{} **{}** :\n".format("Hᴇʟᴘ Fᴏʀ", HELPABLE[module].__MODULE__)
            + HELPABLE[module].__HELP__
        )
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="back"),
                    InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
                ]
            ]
        )
        await query.message.edit(text=text, reply_markup=key)
        
    elif prev_match:
        current_page = int(prev_match.group(1))
        buttons = page_load(current_page - 1, HELPABLE, "help")
        await query.message.edit(
            f"ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ.\nᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ @{SUPPORT_HEHE}\n\n๏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        
    elif next_match:
        current_page = int(next_match.group(1))
        buttons = page_load(current_page + 1, HELPABLE, "help")
        await query.message.edit(
            f"ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ.\nᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ @{SUPPORT_HEHE}\n\n๏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`",
            reply_markup=InlineKeyboardMarkup(buttons)
        )


@app.on_callback_query(filters.regex("home_help"))
async def back(_, query: CallbackQuery):
    buttons = page_load(0, HELPABLE, "help")
    await query.message.edit(
        f"ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ.\nᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ @{SUPPORT_HEHE}\n\n๏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex("back"))
async def back(_, query: CallbackQuery):
    buttons = page_load(0, HELPABLE, "help")
    await query.message.edit(
        f"ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ.\nᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ @{SUPPORT_HEHE}\n\n๏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    
    
@app.on_callback_query(filters.regex("bikash"))
async def back(_, query: CallbackQuery):
    buttons = private_panel()
    await query.message.edit(
        text=f"""ʜᴇʏ {query.from_user.mention}
ᴛʜɪs ɪs {app.mention} ᴀ ᴛᴇʟᴇɢʀᴀᴍ ꜱᴛʀᴇᴀᴍɪɴɢ ʙᴏᴛ ᴡɪᴛʜ ꜱᴏᴍᴇ ᴀᴡᴇꜱᴏᴍᴇ ꜰᴇᴀᴛᴜʀᴇꜱ. ꜱᴜᴘᴘᴏʀᴛɪɴɢ ᴘʟᴀᴛꜰᴏʀᴍꜱ ʟɪᴋᴇ **ʏᴏᴜᴛᴜʙᴇ**, **ꜱᴘᴏᴛɪꜰʏ** ᴇᴛᴄ.

ʙɢᴛ ᴠᴇʀsɪᴏɴ ⊱ `{__Version__}`
ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ ⊱ `{pyver.split()[0]}`
ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ ⊱ `{pyrover}`

**ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ɪɴғᴏ ᴀʙᴏᴜᴛ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs.**""",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
async def help_cmd(_, m: Message):
    try:
        await m.delete()
    except:
        pass
    key = private_help_panel()
    await m.reply_text("ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴍ ғᴏʀ ʜᴇʟᴘ !", reply_markup=InlineKeyboardMarkup(key))
