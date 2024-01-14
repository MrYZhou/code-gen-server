# 使用idea和打包使用
# vscode默认可以在main.py按f5启动

import uvicorn

if __name__ == "__main__":
    # 输出无日志
    # log_path =os.path.join(os.path.expanduser("~"),"laorm","logfile.log")  # Get the name of the script

    # if not os.path.exists(log_path):
    #     os.makedirs(os.path.dirname(log_path), exist_ok=True)
    # log_config = {
    #     "version": 1,
    #     "disable_existing_loggers": True,
    #     "handlers": {
    #         "file_handler": {
    #             "class": "logging.FileHandler",
    #             "filename": log_path,
    #         },
    #     },
    #     "root": {
    #         "handlers": ["file_handler"],
    #         "level": "INFO",
    #     },
    # }
    log_config = {}
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        workers=1,
        log_config=log_config,
    )
