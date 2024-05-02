#bikash
# This module can help you to prevent your group from copyright content. this can delete messages which contains more than 50 words so say fu*k off to the copyright content.
# Pyrogram 2.0 supported module.
# MIT-License copyright own by kopelor 2024-25.
# Delete all admin non admin messages which are blocked.

import re
from pyrogram import Client, filters
from Bgt import app
from pyrogram.types import Message


# Define the maximum length for messages
max_message_length = 200  # Adjust the maximum length as needed


# Event handler to delete long messages
@app.on_message(filters.text & filters.group)
async def delete_long_messages(client, message):
    if len(message.text) > max_message_length:
        await client.delete_messages(message.chat.id, message.id)
        await message.reply_text(f"Hey {message.from_user.mention} Do Not Send More Then 200 Words Text Else Delete Your Message")


# Delete edited messages
@app.on_edited_message(filters.group)
async def delete_edited_messages(client, message):
    await client.delete_messages(message.chat.id, message.id)
    await message.reply_text(f"Hey {message.from_user.mention} Do Not Edit Any Message If You Write Wrong Then Delete And Send Again Else Delete Your Edited Message")


# Delete messages with files
@app.on_message(filters.document & filters.group)
async def delete_file_messages(client, message):
    await client.delete_messages(message.chat.id, message.id)
    await message.reply_text(f"Hey {message.from_user.mention} Do Not Send Any Files Else Delete")

# END
