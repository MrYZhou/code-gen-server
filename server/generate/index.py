# 定义普通方法,组织业务

from dataclasses import replace
import os
import time
from server.generate.dao import Config
from util.cache import LRUCache
from util.base import Common, jinjaEngine, mapKey

# 获取模板解析结果
@LRUCache()
def configParse(key, config: Config):
    res = {}
    basePath = os.path.join(os.getcwd(), "static", "模板" + key)
    modelName = config.name.capitalize()

    for tag in mapKey:
        list = mapKey[tag].get("list")
        for path in list:
            path = tag + path
            template = jinjaEngine.get_template(path)

            baseFile = os.path.basename(path)
            filePath = path
            if tag == "java":
                filePath = path.replace(baseFile, modelName + baseFile)
            folderPath = path.replace(baseFile, "")

            folderPath = folderPath.replace(tag, tag + "/" + config.name, 1)
            filePath = filePath.replace(tag, tag + "/" + config.name, 1)

            targetFolder = os.path.join(basePath, folderPath)
            targetFile = os.path.join(basePath, filePath)

            if not os.path.exists(targetFolder):
                os.makedirs(targetFolder)

            template.stream(config).dump(targetFile)
            res[path] = targetFile
    Common.zipfile(
        os.path.join(os.getcwd(), "static", basePath),
        os.path.join(os.getcwd(), "static", basePath),
    )
    return res


# 使用reder解析
# def parseRender(key, config: Config):
#     res = {}
#     basePath = os.path.join(os.getcwd(), "static", "模板" + key)
#     modelName = config.name.capitalize()
#     for path in list:
#         template = jinjaEngine.get_template(path)
#         content = template.render(config=config)
#         # file = template.stream(content)

#         fileName = path.split("/")[-1]
#         folder = path.replace(fileName, "", 1)
#         path = path.replace(fileName, modelName + fileName, 1)
#         path = path.replace(fileName, modelName + fileName, 1)

#         targetFolder = os.path.join(basePath, config.name, folder)
#         target = os.path.join(basePath, config.name, path)
#         if not os.path.exists(targetFolder):
#             os.makedirs(targetFolder)
#         with open(target, "w", encoding="utf-8") as file:
#             file.write(content)  # 写入模板 生成html

#     # 压缩
#     name = "模板" + key
#     Common.zipfile(
#         os.path.join(os.getcwd(), "static", name),
#         os.path.join(os.getcwd(), "static", name),
#     )
#     res[path] = content
#     return res
