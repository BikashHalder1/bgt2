import config
import asyncio
import importlib
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
from Bgt.logging import LOGGER
from Bgt.core.ptb import ptb
from Bgt.core.userbot import userbot
from Bgt import app, HELPABLE
from Bgt.core.call import JavaCall
from Bgt.plugins import ALL_MODULES
from Bgt.utils.database import get_gbanned, get_banned_users


loop = asyncio.get_event_loop()


async def init():
    
    if not config.STRING1 and not config.STRING2:
        LOGGER("Bgt").error("Atleast Add A Pyrogram V2 String !")
        return
    
    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("Bgt").warning("Fill SPOTIFY_CLIENT_ID & SPOTIFY_CLIENT_SECRET To Play Music From SPOTIFY !")
    
    try:
        users = await get_gbanned()
        for user_id in users:
            config.BANNED_USERS.add(user_id)
        userss = await get_banned_users()
        for user_id in userss:
            config.BANNED_USERS.add(user_id)
    except:
        pass
                
    await app.start()

    for all_module in ALL_MODULES:
        imported_module = importlib.import_module("Bgt.plugins." + all_module)
        if (hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__):
            imported_module.__MODULE__ = imported_module.__MODULE__
            if (hasattr(imported_module, "__HELP__") and imported_module.__HELP__):
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    LOGGER("Bgt.plugins").info("Necessary Modules Imported Successfully !")
    
    await userbot.start()
    await JavaCall.start()
    
    try:
        await JavaCall.stream_call("https://graph.org/file/93882ae5ea01a7bf687b1.jpg")
    except NoActiveGroupCall:
        LOGGER("Bgt").error("[ERROR] - Please Turn On Your Logger Group's Voice Call !")
    except:
        pass
        
    await JavaCall.decorators()
    LOGGER("Bgt").info("Bgt Started Successfully !")
    await idle()


if __name__ == "__main__":
    ptb()
    loop.run_until_complete(init())
    LOGGER("Bgt").info("Stopping Music Bot !")
