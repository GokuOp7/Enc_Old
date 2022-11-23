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
    APP_ID = config("APP_ID", "")
    # APP_ID = "8978848"
    API_HASH = config("API_HASH", "")
    # API_HASH = "24ce3cff2d32cf529df1c0018e28d6cf"
    BOT_TOKEN = config("BOT_TOKEN", "")
    # BOT_TOKEN = "2142121844:AAHgOTKyolhWoifjNGi5lh3j8-VZkeBZrHg"
    DEV = 1995886602
    OWNER = config("OWNER")
    # OWNER = "1995886602"
    FFMPEG = config(
        "FFMPEG",
        default='ffmpeg -i "{}" -preset superfast -c:v libx265 -crf 28 -map 0:v -c:a aac -map 0:a -c:s copy -map 0:s? "{}"',
    )
    # FFMPEG = ""
    THUMB = config(
        "THUMBNAIL", default="https://telegra.ph/file/ab23f5209aae9cae3ba3c.jpg"
    )
    # THUMB = ""
    ICON = config("ICON", default="https://te.legra.ph/file/462b5a002f80bdf8a1ec1.png")
    # ICON = ""
    LOG_CHANNEL = config("LOG_CHANNEL", default="")
    # LOG_CHANNEL = "-1001810558901"
    DBNAME = config("DBNAME", default="TgEncode")
    # DBNAME = ""
    DATABASE_URL = config("DATABASE_URL", default="")
    # DATABASE_URL = "mongodb+srv://Botlover:Botlover@cluster0.e1ymmrm.mongodb.net/?retryWrites=true&w=majority"
except Exception as e:
    print("Environment vars Missing")
    print("something went wrong")
    print(str(e))
    exit()
