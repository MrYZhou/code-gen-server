FROM python:3.10-slim-buster

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple

RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENV PYTHONPATH = /app

CMD ["uvicorn", "main:app","--reload", "--host", "0.0.0.0", "--port", "8000"]

## 网络监听端口

EXPOSE 8000
