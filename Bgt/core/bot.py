import sys
from config import API_ID, API_HASH, BOT_TOKEN, LOG_GROUP_ID
from pyrogram import Client
from Bgt.logging import LOGGER


class MusicBot(Client):
    def __init__(self):
        super().__init__(
            name="Bgt",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            in_memory=True
        )


    async def start(self):
        await super().start()
        get_me = await self.get_me()
        if get_me.last_name:
            self.name = get_me.first_name + "" + get_me.last_name
        else:
            self.name = get_me.last_name
        self.username = get_me.username
        self.mention = get_me.mention
        self.id = get_me.id
        await self.get_chat_member(LOG_GROUP_ID, self.id)
        try:
            LOGGER(__name__).info(f"MusicBot Started As Bgt !")
            await self.send_message(LOG_GROUP_ID, f"**» ʙᴏᴛ sᴛᴀʀᴛᴇᴅ : {self.mention}**")
        except:
            LOGGER(__name__).error("Bot Has Failed To Access The Log Group !")
            sys.exit()


    async def stop(self):
        await super().stop()
        

app = MusicBot()
