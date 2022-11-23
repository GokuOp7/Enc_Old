#FROM python:3.9.2-slim-buster
FROM colserra/ffmpeg:alpha
RUN mkdir /bot && chmod 777 /bot
WORKDIR /bot
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata
RUN apt -qq update && apt -qq install -y git wget pv jq python3-dev mediainfo python3-pip python3
COPY . .
RUN pip install -r requirements.txt
CMD ["bash","run.sh"]`
