from pytgcalls.types import AudioQuality


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
        return AudioQuality.HIGH
    if str(mode) == "High":
        return AudioQuality.HIGH
    elif str(mode) == "Medium":
        return AudioQuality.MEDIUM
    elif str(mode) == "Low":
        return AudioQuality.LOW


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
