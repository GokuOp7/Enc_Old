#    This file is part of the CompressorQueue distribution.
#    Copyright (c) 2021 Danish_00
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
# License can be found in <
# https://github.com/1Danish-00/CompressorQueue/blob/main/License> .

import asyncio
import io
import json
import math
import os
import subprocess
import time
from io import StringIO

from pymongo import MongoClient

from . import *
from .config import *

GROUPENC = []
VERSION2 = []
EVENT2 = []
WORKING = []
QUEUE = {}
OK = {}

FINISHED_PROGRESS_STR = "🧡"
UN_FINISHED_PROGRESS_STR = "🤍"
MAX_MESSAGE_LENGTH = 4096

uptime = dt.now()
os.system(f"wget {THUMB} -O thumb.jpg")
os.system(f"wget {ICON} -O icon.png")

file = open("ffmpeg.txt", "w")
file.write(str(FFMPEG) + "\n")
file.close()

if not os.path.isdir("downloads/"):
    os.mkdir("downloads/")
if not os.path.isdir("encode/"):
    os.mkdir("encode/")
if not os.path.isdir("thumb/"):
    os.mkdir("thumb/")

if DATABASE_URL:
    cluster = MongoClient(DATABASE_URL)
    db = cluster[DBNAME]
    queue = db["queue"]
    ffmpegdb = db["code"]
    filterz = db["filter"]
    queries = queue.find({})
    for query in queries:
        que = str(query["queue"])
        io = StringIO(que)
        pre = json.load(io)
        QUEUE.update(pre)
    queries = ffmpegdb.find({})
    for query in queries:
        que = query["queue"]
        que = que[0]
        io = StringIO(que)
        pre = json.load(io)
        if len(pre) < 5:
            pass
        else:
            file = open("ffmpeg.txt", "w")
            file.write(str(pre) + "\n")
            file.close()
    queries = filterz.find({})
    for query in queries:
        que = query["queue"]
        que = que[0]
        io = StringIO(que)
        pre = json.load(io)
        if len(pre) < 5:
            pass
        else:
            file = open("filter.txt", "w")
            file.write(str(pre) + "\n")
            file.close()
else:
    ffmpegdb = ""
    filterz = ""


def stdr(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if len(str(minutes)) == 1:
        minutes = "0" + str(minutes)
    if len(str(hours)) == 1:
        hours = "0" + str(hours)
    if len(str(seconds)) == 1:
        seconds = "0" + str(seconds)
    dur = (
        ((str(hours) + ":") if hours else "00:")
        + ((str(minutes) + ":") if minutes else "00:")
        + ((str(seconds)) if seconds else "")
    )
    return dur


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
    )
    return tmp[:-2]


def ts(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
        + ((str(milliseconds) + "ms, ") if milliseconds else "")
    )
    return tmp[:-2]


def hbs(size):
    if not size:
        return ""
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "B", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


No_Flood = {}


async def progress_for_pyrogram(current, total, bot, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        status = "downloads" + "/status.json"
        if os.path.exists(status):
            with open(status, "r+") as f:
                statusMsg = json.load(f)
                if not statusMsg["running"]:
                    bot.stop_transmission()
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "{0}{1} \n<b>Progress:</b> {2}%\n".format(
            "".join(
                [FINISHED_PROGRESS_STR for i in range(math.floor(percentage / 10))]
            ),
            "".join(
                [
                    UN_FINISHED_PROGRESS_STR
                    for i in range(10 - math.floor(percentage / 10))
                ]
            ),
            round(percentage, 2),
        )

        tmp = progress + "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(
            hbs(current),
            hbs(total),
            hbs(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != "" else "0 s",
        )
        try:
            if not message.photo:
                await message.edit_text(text="{}\n {}".format(ud_type, tmp))
            else:
                await message.edit_caption(caption="{}\n {}".format(ud_type, tmp))
        except BaseException:
            pass


async def progress(current, total, event, start, type_of_ps, file=None):
    now = time.time()
    if No_Flood.get(event.chat_id):
        if No_Flood[event.chat_id].get(event.id):
            if (now - No_Flood[event.chat_id][event.id]) < 1.1:
                return
        else:
            No_Flood[event.chat_id].update({event.id: now})
    else:
        No_Flood.update({event.chat_id: {event.id: now}})
    diff = time.time() - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        time_to_completion = round((total - current) / speed) * 1000
        progress_str = "**Progress**: `{0}{1} {2}%` \n".format(
            "".join(["🧡" for i in range(math.floor(percentage / 10))]),
            "".join(["🤍" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 4),
        )
        tmp = (
            progress_str
            + "**Completed**: `{0} of {1}`\n**Speed**: `{2}/s` \n**ETA**: `{3}` \n".format(
                hbs(current),
                hbs(total),
                hbs(speed),
                ts(time_to_completion),
            )
        )
        if file:
            await event.edit(
                "`✦ {}`\n\n`File Name: {}`\n\n{}".format(type_of_ps, file, tmp)
            )
        else:
            await event.edit("`✦ {}`\n\n{}".format(type_of_ps, tmp))


async def info(file, event):
    process = subprocess.Popen(
        ["mediainfo", file, "--Output=HTML"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    stdout, stderr = process.communicate()
    out = stdout.decode()
    client = TelegraphPoster(use_api=True)
    client.create_api_token("Mediainfo")
    page = client.post(
        title="Mediainfo",
        author="ANi_MiRROR",
        author_url="https://t.me/Ani_Mirror",
        # author=((await event.client.get_me()).first_name),
        # author_url=f"https://t.me/{((await
        # event.client.get_me()).username)}",
        text=out,
    )
    return page["url"]


def code(data):
    OK.update({len(OK): data})
    return str(len(OK) - 1)


def decode(key):
    if OK.get(int(key)):
        return OK[int(key)]
    return


async def skip(e):
    wah = e.pattern_match.group(1).decode("UTF-8")
    wh = decode(wah)
    out, dl, id = wh.split(";")
    try:
        # if QUEUE.get(int(id)):
        if QUEUE.get(id):
            WORKING.clear()
            # QUEUE.pop(int(id))
            QUEUE.pop(id)
            await save2db()
        await e.delete()
        os.remove(dl)
        os.remove(out)
        # Lets kill ffmpeg else it will run in memory even after deleting
        # input.
        for proc in psutil.process_iter():
            processName = proc.name()
            processID = proc.pid
            print(processName, " - ", processID)
            if processName == "ffmpeg":
                os.kill(processID, signal.SIGKILL)
    except BaseException:
        pass
    return


async def fast_download(e, download_url, filename=None):
    def progress_callback(d, t):
        return (
            asyncio.get_event_loop().create_task(
                progress(
                    d,
                    t,
                    e,
                    time.time(),
                    f"Downloading from {download_url}",
                )
            ),
        )

    async def _maybe_await(value):
        if inspect.isawaitable(value):
            return await value
        else:
            return value

    async with aiohttp.ClientSession() as session:
        async with session.get(download_url, timeout=None) as response:
            if not filename:
                filename = download_url.rpartition("/")[-1]
            filename = os.path.join("downloads", filename)
            total_size = int(response.headers.get("content-length", 0)) or None
            downloaded_size = 0
            with open(filename, "wb") as f:
                async for chunk in response.content.iter_chunked(1024):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        await _maybe_await(
                            progress_callback(downloaded_size, total_size)
                        )
            return filename
