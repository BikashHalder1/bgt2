import sys
import config
from pyrogram import Client
from Bgt.logging import LOGGER


assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="Bgt1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1)
        )
        self.two = Client(
            name="Bgt2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2)
        )
        self.three = Client(
            name="Bgt3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3)
        )
        self.four = Client(
            name="Bgt4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4)
        )
        self.five = Client(
            name="Bgt5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5)
        )

    
    async def start(self):
        LOGGER(__name__).info(f"Getting Assistants Info")
        if config.STRING1:
            await self.one.start()
            try:
                await self.one.join_chat("Bgt_Chat")
            except:
                pass
            assistants.append(1)
            get_me = await self.one.get_me()
            self.one.username = get_me.username
            self.one.id = get_me.id
            self.one.mention = get_me.mention
            assistantids.append(get_me.id)
            LOGGER(__name__).info(f"Assistant One Started")
            try:
                await self.one.send_message(config.LOG_GROUP_ID, f"**» ᴀssɪsᴛᴀɴᴛ ᴏɴᴇ sᴛᴀʀᴛᴇᴅ :** {self.one.mention}")
            except:
                LOGGER(__name__).error(f"Assistant Account 1 Has Failed To Access The Log Group")
                sys.exit()

        if config.STRING2:
            await self.two.start()
            try:
                await self.two.join_chat("Bgt_Chat")
            except:
                pass
            assistants.append(2)
            get_me = await self.two.get_me()
            self.two.username = get_me.username
            self.two.id = get_me.id
            self.two.mention = get_me.mention
            assistantids.append(get_me.id)
            LOGGER(__name__).info(f"Assistant Two Started")
            try:
                await self.two.send_message(config.LOG_GROUP_ID, f"**» ᴀssɪsᴛᴀɴᴛ ᴛᴡᴏ sᴛᴀʀᴛᴇᴅ :** {self.two.mention}")
            except:
                LOGGER(__name__).error(f"Assistant Account 2 Has Failed To Access The Log Group")
                sys.exit()
                
        if config.STRING3:
            await self.three.start()
            try:
                await self.three.join_chat("Bgt_Chat")
            except:
                pass
            assistants.append(3)
            get_me = await self.three.get_me()
            self.three.username = get_me.username
            self.three.id = get_me.id
            self.three.mention = get_me.mention
            assistantids.append(get_me.id)
            LOGGER(__name__).info(f"Assistant three Started")
            try:
                await self.three.send_message(config.LOG_GROUP_ID, f"**» ᴀssɪsᴛᴀɴᴛ ᴛʜʀᴇᴇ sᴛᴀʀᴛᴇᴅ :** {self.three.mention}")
            except:
                LOGGER(__name__).error(f"Assistant Account 3 Has Failed To Access The Log Group")
                sys.exit()

        if config.STRING4:
            await self.four.start()
            try:
                await self.four.join_chat("Bgt_Chat")
            except:
                pass
            assistants.append(4)
            get_me = await self.four.get_me()
            self.four.username = get_me.username
            self.four.id = get_me.id
            self.four.mention = get_me.mention
            assistantids.append(get_me.id)
            LOGGER(__name__).info(f"Assistant four Started")
            try:
                await self.four.send_message(config.LOG_GROUP_ID, f"**» ᴀssɪsᴛᴀɴᴛ ғᴏᴜʀ sᴛᴀʀᴛᴇᴅ :** {self.four.mention}")
            except:
                LOGGER(__name__).error(f"Assistant Account 4 Has Failed To Access The Log Group")
                sys.exit()
                
        if config.STRING5:
            await self.five.start()
            try:
                await self.five.join_chat("Bgt_Chat")
            except:
                pass
            assistants.append(5)
            get_me = await self.five.get_me()
            self.five.username = get_me.username
            self.five.id = get_me.id
            self.five.mention = get_me.mention
            assistantids.append(get_me.id)
            LOGGER(__name__).info(f"Assistant five Started")
            try:
                await self.four.send_message(config.LOG_GROUP_ID, f"**» ᴀssɪsᴛᴀɴᴛ ғɪᴠᴇ sᴛᴀʀᴛᴇᴅ :** {self.five.mention}")
            except:
                LOGGER(__name__).error(f"Assistant Account 5 Has Failed To Access The Log Group")
                sys.exit()                
            

userbot = Userbot()
