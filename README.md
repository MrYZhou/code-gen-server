# code-gen-server

fastapi document
[https://fastapi.tiangolo.com/zh/tutorial/first-steps/](https://fastapi.tiangolo.com/zh/tutorial/first-steps/)

jinja2 document
[http://docs.jinkan.org/docs/jinja2/index.html](http://docs.jinkan.org/docs/jinja2/index.html)

## step:
1: install dependencies
```bash
poetry update
```
2.Prepare Redis and listen on port 6379.

3.Prepare the MySQL database and load/execute the SQL statements in the init.sql file located in the current directory.

4.start project
```bash
f5 or run main.py
```

## build app
if you want build a docker image,you can use dockerfile.
such as
```bash
docker build -t fastweb .
docker run -d -p 8000:8000 fastweb
```
or build executable file
```bash
python -m build.py
```



