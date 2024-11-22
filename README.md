# code-gen-server

## 结构

- router 编写接口的
- template 放代码生成模板
- util 放系统的工具类和项目配置等代码

## 开始

### 1: 安装 poetry 后换源下载依赖

```bash
pip install poetry
poetry config repositories.pypi https://pypi.tuna.tsinghua.edu.cn/simple/
poetry update
```

### 2.使用 redis 监听 6379（可选）

```dockerfile
docker run --restart=always --name redis -d -p 6379:6379 redis
```

### 3.init.sql 文件是数据库初始化文件，先创建数据库 study，然后导入 init.sql 文件。

### 4.创建.env 文件，内容参考如下,可以动态修改数据库配置

### 5.提交格式化钩子

```bash
pre-commit install
pre-commit run --all-files
auto-commit.bat
```

```bash
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=study
```

### 5.启动项目

```bash
f5
```

## 部署

docker 镜像

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
