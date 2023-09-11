command = []

cleanmode = []


async def is_commanddelete_on(chat_id: int) -> bool:
    if chat_id not in command:
        return True
    else:
        return False

async def commanddelete_off(chat_id: int):
    if chat_id not in command:
        command.append(chat_id)

async def commanddelete_on(chat_id: int):
    try:
        command.remove(chat_id)
    except:
        pass


async def is_cleanmode_on(chat_id: int) -> bool:
    if chat_id not in cleanmode:
        return True
    else:
        return False

async def cleanmode_off(chat_id: int):
    if chat_id not in cleanmode:
        cleanmode.append(chat_id)

async def cleanmode_on(chat_id: int):
    try:
        cleanmode.remove(chat_id)
    except:
        pass
