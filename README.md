# fastapi-le

fastapi document
[https://fastapi.tiangolo.com/zh/tutorial/first-steps/](https://fastapi.tiangolo.com/zh/tutorial/first-steps/)
orm document
[https://sqlmodel.tiangolo.com/tutorial/](https://sqlmodel.tiangolo.com/tutorial/)
## use:
```java
1: need build a venv folder
python -m venv .venv
2.start venv
.\.venv\Scripts\activate 
3.install pacakge
pip install -r requirements.txt
4.start app
uvicorn main:app --reload --port=8000
```

## build app
```java
docker-compose up -d
```
if you want build a docker images,you can use dockerfile.
such as
```java
docker build -t fastweb .
```

## about dependency
```java
walrus 限流

fastapi相关
fastapi
uvicorn[standard]

模板引擎
jinja2

文件
aiofiles

#orm操作
sqlmodel 模型支持(pydantic和SQLAlchemy之上的一个封装,使得与两者的工作变得容易。是fastapi作者为了简化数据库操作而设计的,对fastapi框架兼容最好)
pymysql  数据库驱动
```