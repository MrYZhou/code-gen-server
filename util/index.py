import zipfile
import os

class Common:
    @staticmethod
    def zipfile(src_dir, save_name='default'):
        '''
        压缩整个文件夹
        压缩文件夹下所有文件及文件夹
        默认压缩文件名：文件夹名
        默认压缩文件路径：文件夹上层目录
        '''
        if save_name == 'default':
            zip_name = src_dir + '.zip'
        else:
            if save_name is None or save_name == '':
                zip_name = src_dir + '.zip'
            else:
                zip_name = save_name + '.zip'

        z = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(src_dir):
            fpath = dirpath.replace(src_dir, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
        z.close()
        return True
    @staticmethod
    def unzipfile(zip_src, dst_dir):
        '''
        解压缩
        '''
        r = zipfile.is_zipfile(zip_src)
        if r:
            fz = zipfile.ZipFile(zip_src, 'r')
            for file in fz.namelist():
                fz.extract(file, dst_dir)
        else:
            print('This is not zip')
            return False
        return True
