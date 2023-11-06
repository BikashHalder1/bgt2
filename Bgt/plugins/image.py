import api = SafoneAPI()

from pyrogram import *
from pyrogram.types import *
from Bgt.utils.inline import *

img_db = {}

async def add_img(user_id, resu, sent):
    put_img = {
        "user_id": user_id,
        "resu" : resu,
        "sent": sent,
    }
    if user_id in img_db:
        img_db.pop(user_id)
    img_db[user_id] = []
    img_db[user_id].append(put_img)
    return
    

    

@app.on_message(filters.command("image"))
async def image_search(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
          text="**Please Give Some Query\nTo Get Images !**"
        )
    user_id = message.from_user.id
    try:
        await message.delete()
    except:
        pass
    try:
        m = await message.reply_text("**Searching ...**")
        text = message.text.split(None, 1)[1]
        resp = await api.image(text, 100)
        resu = resp.results
        sent = 0
        image = resu[sent].imageUrl
        caption = resu[sent].title
        buttons = image_markup(user_id)
        await m.delete()
        await message.reply_photo(
            photo=image,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        await add_img(user_id, resu, sent)
        
    except:
        pass
        return await message.reply_text(
                text="**Not Found, Please Try To\nSearch Another Image ...**"
        )

@app.on_callback_query(filters.regex("change_images"))
async def change_imagex(client, query: CallbackQuery):
    await query.answer()
    user_id = query.from_user.id
    if user_id not in img_db:
        return await query.answer(
            f"Something Went Wrong ...",
            show_alert=True,
        )
    check = img_db.get(user_id)
    user_id = check[0]["user_id"]
    resu = check[0]["resu"]
    sent = check[0]["sent"]
    try:
        curr = sent + 1
        new = {"sent": curr}
        check[0].update(new)
        image = resu[curr].imageUrl
        caption = resu[curr].title
    except:
        curr = sent + 2
        new = {"sent": curr}
        check[0].update(new)
        image = resu[curr].imageUrl
        caption = resu[curr].title
        pass
    buttons = image_markup(user_id)
    await query.edit_message_media(
        media = InputMediaPhoto(
            media=f"{image}",
            caption=f"{caption}",
        ),
        reply_markup = InlineKeyboardMarkup(buttons),
    )



__MODULE__ = "Image"
__HELP__ = """
**Get Various Types of Images**

/image [image type] - Get Image
Which You Want.

**Ex:** `/image Shree Ram"""