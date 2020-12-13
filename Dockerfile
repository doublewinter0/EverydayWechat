FROM python:alpine

ENV TZ Asia/Shanghai
ENV MODE server

LABEL maintainer="erdong.ren@gamil.com"
LABEL version="1.1.0"

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories

RUN apk update && apk add --virtual build-dependencies \
    build-base \
    libxml2-dev \
    libxslt-dev

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN apk del build-dependencies \
    && rm -rf /var/cache/apk/*

COPY . .

CMD ["python", "run.py"]
