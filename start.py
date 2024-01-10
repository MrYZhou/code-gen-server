# 使用idea和打包使用,reload=False否则打包exe会无限reload。
# vscode默认可以在main.py按f5启动

import os
import uvicorn

if __name__ == "__main__":
    name_app = os.path.basename(__file__)[0:-3]  # Get the name of the script
    log_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "handlers": {
            "file_handler": {
                "class": "logging.FileHandler",
                "filename": "logfile.log",
            },
        },
        "root": {
            "handlers": ["file_handler"],
            "level": "INFO",
        },
    }
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=False, workers=1,log_config=log_config)
