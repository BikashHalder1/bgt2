FROM nikolaik/python-nodejs:python3.11-nodejs18

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/

WORKDIR /app/

RUN pip3 install --no-cache-dir --upgrade --requirement Installer
RUN python3 -m pip install -U https://github.com/coletdjnz/yt-dlp-youtube-oauth2/archive/refs/heads/master.zip
RUN mkdir ${XDG_CONFIG_HOME}/yt-dlp
RUN echo "--username oauth2 --password ''" > ${XDG_CONFIG_HOME}/yt-dlp/config
RUN yt-dlp https://youtube.com/shorts/KNu5Kn6keyw

CMD python3 -m Bgt
