import os
import random
import re
import string
import zipfile

from fastapi.templating import Jinja2Templates


# 模板初始化
jinjaEngine = Jinja2Templates("template")


class Common:
    @staticmethod
    def tocamel(name: str) -> str:
        """下划线转驼峰(小驼峰)"""
        return re.sub(r"(_[a-z])", lambda x: x.group(1)[1].upper(), name)

    @staticmethod
    def tosnake(name: str) -> str:
        """驼峰转下划线"""
        if "_" in name:
            raise ValueError(f"{name}字符中包含下划线，无法转换")
        return re.sub(r"([a-z])([A-Z])", r"\1_\2", name).lower()

    @staticmethod
    def randomkey(len: int = 10):
        return "".join(random.sample(string.ascii_letters + string.digits, len))

    @staticmethod
    def zipfile(src_dir, save_name):
        """
        压缩整个文件夹
        压缩文件夹下所有文件及文件夹
        默认压缩文件名：文件夹名
        默认压缩文件路径：文件夹上层目录
        """
        zip_name = save_name + ".zip"
        if save_name is None or save_name == "":
            zip_name = src_dir + ".zip"

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


