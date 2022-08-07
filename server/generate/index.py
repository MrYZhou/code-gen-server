
# 定义普通方法,组织业务

import os
import time
from server.generate.dao import Config
from util.cache import LRUCache
from util.base import jinjaEngine

# 获取模板解析结果
@LRUCache()
def configParse(key,config:Config):
  print('模板渲染')
  list = ['java/model/Info.java',
          'java/model/Query.java',
          'java/Controller.java',
          'java/Entity.java',
          'java/model.xml',
          'java/Repository.java',
          'java/Service.java',
          'mobile/index.vue',
          'mobile/form.vue',
          'web/index.vue',
          'web/form.vue',
         ]
  res = {}
  basePath =os.path.join(os.getcwd(),'static','模板'+key)
  modelName = config.name.capitalize()
  for path in list:
    template = jinjaEngine.get_template(path)  
    content = template.render(config = config)
    # file = template.stream(content)
    
    fileName = path.split("/")[-1]
    folder = path.replace(fileName,'',1)
    path = path.replace(fileName,modelName+fileName,1)
    targetFolder = os.path.join(basePath,config.name,folder)
    target = os.path.join(basePath,config.name,path)
    if not os.path.exists(targetFolder):
      os.makedirs(targetFolder)
    with open (target , 'w', encoding='utf-8' ) as file:
      file.write(content)  # 写入模板 生成html  
    res[path] = content
  return res
