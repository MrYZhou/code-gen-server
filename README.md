# code-gen-server

fastapi document
[https://fastapi.tiangolo.com/zh/tutorial/first-steps/](https://fastapi.tiangolo.com/zh/tutorial/first-steps/)

jinja2 document
[http://docs.jinkan.org/docs/jinja2/index.html](http://docs.jinkan.org/docs/jinja2/index.html)

## step:
1: need build a venv folder
```bash
python -m venv .venv
```
2.start venv
```bash
.\.venv\Scripts\activate 
```
3.install pacakge
```bash
pip install -r requirements.txt
```
4.start app
```bash
uvicorn main:app --reload --port=8000
```
5.add a dotenv file (optional)
```python
DB_HOST = "192.168.20.43"
DB_PORT = "3306"
DB_USER = "root"
DB_PASSWORD = "123456"
DB_NAME = "study"
DB_DRIVER = "mysql+pymysql"
SQLMODEL_ECHO = True
```

## build app
```bash
docker-compose up -d
```
if you want build a docker image,you can use dockerfile.
such as
```bash
docker build -t fastweb .
docker run -d -p 8000:8000 fastweb
```


