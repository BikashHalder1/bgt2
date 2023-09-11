from pytgcalls.types import (HighQualityAudio, HighQualityVideo, LowQualityAudio,
                         LowQualityVideo, MediumQualityAudio, MediumQualityVideo)


audio = {}

video = {}


async def save_audio_bitrate(chat_id: int, bitrate: str):
    audio[chat_id] = bitrate


async def save_video_bitrate(chat_id: int, bitrate: str):
    video[chat_id] = bitrate


async def get_aud_bit_name(chat_id: int) -> str:
    mode = audio.get(chat_id)
    if not mode:
        return "High"
    return mode


async def get_vid_bit_name(chat_id: int) -> str:
    mode = video.get(chat_id)
    if not mode:
        return "High"
    return mode


async def get_audio_bitrate(chat_id: int) -> str:
    mode = audio.get(chat_id)
    if not mode:
        return MediumQualityAudio()
    if str(mode) == "High":
        return HighQualityAudio()
    elif str(mode) == "Medium":
        return MediumQualityAudio()
    elif str(mode) == "Low":
        return LowQualityAudio()


async def get_video_bitrate(chat_id: int) -> str:
    mode = video.get(chat_id)
    if not mode:
        return HighQualityVideo()
    if str(mode) == "High":
        return HighQualityVideo()
    elif str(mode) == "Medium":
        return MediumQualityVideo()
    elif str(mode) == "Low":
        return LowQualityVideo()
