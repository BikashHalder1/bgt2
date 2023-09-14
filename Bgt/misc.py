import config
import socket
import heroku3
from pyrogram import filters
from Bgt.logging import LOGGER
from Bgt.core.mongo import pymongodb


SUDOERS = filters.user()


HAPP = None


db = {}


def is_heroku():
    return "heroku" in socket.getfqdn()


XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(config.HEROKU_API_KEY),
    "https",
    str(config.HEROKU_APP_NAME),
    "HEAD",
    "main",
]


def dbb():
    global db
    db = db
    LOGGER(__name__).info("Database Loaded !")


def sudo():
    global SUDOERS
    OWNER = config.OWNER_ID
    try:
        sudoersdb = pymongodb.sudoers
        sudoers = sudoersdb.find_one({"sudo": "sudo"})
        sudoers = [] if not sudoers else sudoers["sudoers"]
        for user_id in OWNER:
            SUDOERS.add(user_id)
            if user_id not in sudoers:
                sudoers.append(user_id)
                sudoersdb.update_one(
                    {"sudo": "sudo"},
                    {"$set": {"sudoers": sudoers}},
                    upsert=True,
                )
        if sudoers:
            for x in sudoers:
                SUDOERS.add(x)
    except Exception as e:
        print(e)            
    LOGGER(__name__).info("Sudo Users Loaded Successfully !")


def heroku():
    global HAPP
    if is_heroku:
        if config.HEROKU_API_KEY and config.HEROKU_APP_NAME:
            try:
                Heroku = heroku3.from_key(config.HEROKU_API_KEY)
                HAPP = Heroku.app(config.HEROKU_APP_NAME)
                LOGGER(__name__).info("Heroku App Configured Successfully !")
            except BaseException:
                LOGGER(__name__).warning("Please Make Sure Your Heroku API Key And Your App Name Are Configured Correctly In The Heroku !")
