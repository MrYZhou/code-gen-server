FROM python:alpine3.16

COPY ./requirements.txt /app/requirements.txt

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN apk add --no-cache --virtual build-dependencies \
  python3-dev \
  libffi-dev \
  openssl-dev \
  gcc \
  libc-dev \
  linux-headers \
  freetds-dev \
  make

RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple


RUN pip3 install -r /app/requirements.txt


RUN apk del build-dependencies

COPY . /app

WORKDIR /app

CMD [ "uvicorn" ,"main:app","--host" ,"0.0.0.0","--reload"]

## 网络监听端口
EXPOSE 8000