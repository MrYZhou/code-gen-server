
# 定义普通方法,组织业务

from util.cache import LRUCache
from util.base import jinjaEngine

# 获取模板解析结果
@LRUCache()
def configParse(key,config):
  print('模板渲染')
  content=''
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
  for path in list:
    template = jinjaEngine.get_template(path)  
    file = template.stream(content)
    res[path] = file
  
  
  return res
