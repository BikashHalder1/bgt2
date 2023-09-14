import sys
from os import remove, listdir, mkdir
from Bgt.logging import LOGGER


def dirr():
    if "assets" not in listdir("Bgt"):
        LOGGER(__name__).warning("Assets Folder Not Found !")
        sys.exit()

    for file in listdir():
        if file.endswith(".jpg"):
            remove(file)
            
    for file in listdir():
        if file.endswith(".jpeg"):
            remove(file)

    if "downloads" not in listdir():
        mkdir("downloads")
        
    if "cache" not in listdir():
        mkdir("cache")
    
