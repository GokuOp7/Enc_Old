#    This file is part of the Compressor distribution.
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
from decouple import config

# For Local deployment uncomment the commented variables and comment the
# uncommented ines


try:
    APP_ID = config("APP_ID", default=6, cast=int)
    # APP_ID = ""
    API_HASH = config("API_HASH", default="eb06d4abfb49dc3eeb1aeb98ae0f581e")
    # API_HASH = ""
    BOT_TOKEN = config("BOT_TOKEN")
    # BOT_TOKEN = ""
    DEV = 1322549723
    OWNER = config("OWNER")
    # OWNER = ""
    FFMPEG = config(
        "FFMPEG",
        default='ffmpeg -i "{}" -preset ultrafast -c:v libx265 -crf 27 -map 0:v -c:a aac -map 0:a -c:s copy -map 0:s? "{}"',
    )
    # FFMPEG = ""
    THUMB = config(
        "THUMBNAIL", default="https://telegra.ph/file/ab23f5209aae9cae3ba3c.jpg"
    )
    # THUMB = ""
    ICON = config("ICON", default="https://te.legra.ph/file/462b5a002f80bdf8a1ec1.png")
    # ICON = ""
    LOG_CHANNEL = config("LOG_CHANNEL", default="")
    # LOG_CHANNEL = ""
    DBNAME = config("DBNAME", default="TgEncode")
    # DBNAME = ""
    DATABASE_URL = config("DATABASE_URL", default="")
    # DATABASE_URL = ""
except Exception as e:
    print("Environment vars Missing")
    print("something went wrong")
    print(str(e))
    exit()
