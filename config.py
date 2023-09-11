from os import getenv, path
from dotenv import load_dotenv
from pyrogram import filters


if path.exists("Internal"):
    load_dotenv("Internal")
    
    
#----------------------------------REQUIRED-------------------------------#


API_ID = int(getenv("API_ID", None))

API_HASH = getenv("API_HASH", None)

BOT_TOKEN = getenv("BOT_TOKEN", None)

MONGO_DB = getenv("MONGO_DB", None)

STRING1 = getenv("STRING1", None)

LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", None))

OWNER_ID = list(map(int, getenv("OWNER_ID").split()))


#----------------------------OPTIONAL--------------------------------#


STRING2 = getenv("STRING2", None)
STRING3 = getenv("STRING3", None)
STRING4 = getenv("STRING4", None)
STRING5 = getenv("STRING5", None)

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", "900"))

SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "900"))

HEROKU_API_KEY = getenv("HEROKU_API_KEY", None)

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", None)

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/BikashHalder1/Bgt2")

UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "bikash")

GIT_TOKEN = getenv("GIT_TOKEN", None)

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/BikashGadgetsTech")

SUPPORT_GROUP = getenv("SUPPORT_GROUP", "https://t.me/Bgt_Chat")

SUPPORT_HEHE = SUPPORT_GROUP.split("me/")[1]

AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "False")

AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "54000"))

AUTO_DOWNLOADS_CLEAR = getenv("AUTO_DOWNLOADS_CLEAR", "True")

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "04bd2cf9ebad4b6cb54b0e24a039b15e")

SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "ac02869b41964e349fcda21cd87a902c")

VIDEO_STREAM_LIMIT = int(getenv("VIDEO_STREAM_LIMIT", "50"))

SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "200"))

PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "100"))

CLEAN_MINS = int(getenv("CLEANMODE_MINS", "15"))

TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "104857600"))

TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "10737418240"))


#--------------------------DIRECTORIES--------------------------#


HELPABLE = {}

LOAD = []

NO_LOAD = []

BANNED_USERS = filters.user()

lyrical = {}

chatstats = {}

userstats = {}

clean = {}

autoclean = []


#----------------------------------------IMAGES-------------------------------------------#


START_IMG = getenv("START_IMG", "https://graph.org/file/d4bc06ada79821eb01025.jpg")

EXTRA_IMG = getenv("EXTRA_IMG", "https://te.legra.ph/file/2e2741f5dfe9f62eed91d.png")

STREAM_IMG = getenv("STREAM_IMG", "https://graph.org/file/93882ae5ea01a7bf687b1.jpg")


#-------------------------------------FUNCTION---------------------------------------#


def time_to_seconds(time):
    stringt = str(time)
    return sum(
        int(x) * 60**i
        for i, x in enumerate(reversed(stringt.split(":")))
    )


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

SONG_DOWNLOAD_DURATION_LIMIT = int(time_to_seconds(f"{SONG_DOWNLOAD_DURATION}:00"))
