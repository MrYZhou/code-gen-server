import os
import random
import re
import string
import zipfile

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

# 模板初始化
jinjaEngine = Jinja2Templates("")
routeList = []


def registe(router: APIRouter):
    routeList.append(router)


class Common:

    @staticmethod
    def _name_convert_to_camel(name: str) -> str:
        """下划线转驼峰(小驼峰)"""
        return re.sub(r'(_[a-z])', lambda x: x.group(1)[1].upper(), name)

    @staticmethod
    def _name_convert_to_snake(name: str) -> str:
        """驼峰转下划线"""
        if '_' not in name:
            name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
        else:
            raise ValueError(f'{name}字符中包含下划线，无法转换')
        return name.lower()
    @staticmethod
    def randomkey(len: int = 10):
        return "".join(random.sample(string.ascii_letters + string.digits, len))

    @staticmethod
    def zipfile(src_dir, save_name="default"):
        """
        压缩整个文件夹
        压缩文件夹下所有文件及文件夹
        默认压缩文件名：文件夹名
        默认压缩文件路径：文件夹上层目录
        """
        if save_name == "default":
            zip_name = src_dir + ".zip"
        else:
            if save_name is None or save_name == "":
                zip_name = src_dir + ".zip"
            else:
                zip_name = save_name + ".zip"

        z = zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(src_dir):
            fpath = dirpath.replace(src_dir, "")
            fpath = fpath and fpath + os.sep or ""
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
        z.close()
        return True

    @staticmethod
    def unzipfile(zip_src, dst_dir):
        """
        解压缩
        """
        r = zipfile.is_zipfile(zip_src)
        if r:
            fz = zipfile.ZipFile(zip_src, "r")
            for file in fz.namelist():
                fz.extract(file, dst_dir)
        else:
            print("This is not zip")
            return False
        return True


class App:
    def __init__(self):
        self.je = jinjaEngine


# 通用常量
mapKey = {
    "java": {
        "list": [
            "Info.java",
            "Query.java",
            "Controller.java",
            "Entity.java",
            "Model.xml",
            "Mapper.java",
            "Service.java",
            "ServiceImpl.java"
        ]
    },
    "mobile": {
        "list": [
            "/index.vue",
            "/form.vue",
        ]
    },
    "web": {
        "list": [
            "/index.vue",
            "/form.vue",
        ]
    },
}
