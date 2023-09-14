from config import BOT_TOKEN
import telegram.ext as tg


updater = tg.Updater(BOT_TOKEN, use_context=True)

dispatcher = updater.dispatcher


def ptb():
    updater.start_polling()
