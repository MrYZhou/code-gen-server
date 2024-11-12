# code-gen-server



## step:
1: 安装poetry后换源下载依赖
```bash
pip install poetry
poetry config repositories.pypi https://pypi.tuna.tsinghua.edu.cn/simple/
poetry update
```
2.使用redis监听 6379.

3.init.sql文件是数据库初始化文件，先创建数据库study，然后导入init.sql文件。

4.创建.env文件，内容如下,可以动态修改数据库配置
```bash
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=study
```

5.启动项目
```bash
f5 or run main.py
```

## 部署
docker镜像
```bash
docker build -t fastweb .
docker run -d -p 8000:8000 fastweb
```
可执行文件
```bash
python  build.py
```

## 其他

fastapi 文档
[https://fastapi.tiangolo.com/zh/tutorial/first-steps/](https://fastapi.tiangolo.com/zh/tutorial/first-steps/)

jinja2 模板引擎文档
[http://docs.jinkan.org/docs/jinja2/index.html](http://docs.jinkan.org/docs/jinja2/index.html)


