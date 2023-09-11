import time
from aiohttp import ClientSession
from config import HELPABLE
from Bgt.core.bot import app
from Bgt.core.git import git
from Bgt.core.dir import dirr
from Bgt.misc import dbb, heroku, sudo


__Version__ = "0.2.4"

boot = time.time()

dirr()

git()

dbb()

heroku()

sudo()

app = app

aiohttpsession = ClientSession()

HELPABLE = HELPABLE
