# Version: 0.0.1
FROM ubuntu
MAINTAINER Ivan V. Protchenko <protchenko.vanya@gmail.com>
COPY . /app
RUN apt update \
&& apt upgrade -y \
&& apt install -y python3-pip \
&& pip3 install -r /app/requirements.txt \
&& rm -rf /var/lib/apt/lists/*
WORKDIR /app
ENTRYPOINT ["/app/boot.sh"]
#docker build -t ivanprotchenko/davlenie -f Dockerfile .