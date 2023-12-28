# 定义普通方法,组织业务

from glob import iglob
import os
from pathlib import Path as op
from dataclasses import field, replace

from server.generate.dao import Config
from util.base import Common, jinjaEngine, mapKey

def configParse(key, config: Config):
    res = {}
    basePath = op.joinpath(os.getcwd(), "static", "模板" + key)
    modelName = config.name.capitalize()

    # 获取java
    list = iglob("template/java/*")
    tag = "java"
    for path in list:
        path = tag + path
        template = jinjaEngine.get_template(path)

        baseFile = os.path.basename(path)
        filePath = path
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


# 命令行使用
async def configGen(list, dataBase):
    # 过滤前缀
    tablePrefix = dataBase["prefix"]["table"]
    fieldPrefix = dataBase["prefix"]["field"]

    # 生成目录信息
    table = dataBase["table"]
    modelName = dataBase["table"].replace(tablePrefix, "").capitalize()
    downName = modelName + "-" + Common.randomkey()
    basePath = os.path.join(os.getcwd(), "static", downName)
    if not os.path.exists(basePath):
        os.makedirs(basePath)

    # 提供给模板文件的数据
    config = {
        "list": list,
        "table": Common.tocamel(table.replace(tablePrefix, "")),
        "tableName": table,
        "modelName": Common.tocamel(modelName),
        "fieldPrefix": fieldPrefix,
        "searchList": dataBase["searchList"],
    }

    # 遍历模板文件生成代码
    fileList = mapKey["java"].get("list")
    for genFile in fileList:
        targetFile = os.path.join(basePath, Common.tocamel(modelName) + genFile)

        templatePath = "java/" + genFile
        template = jinjaEngine.get_template(templatePath)
        template.stream(config=config).dump(targetFile)

    # 压缩文件
    target = os.path.join(os.getcwd(), "static", basePath)
    Common.zipfile(target, target)
    return downName


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
