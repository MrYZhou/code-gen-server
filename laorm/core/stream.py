import inspect
import re
from typing import TypeVar
from abc import ABCMeta
from . import PPA


class SqlStateMachine:
    def __init__(self, *args):
        self.mode = "select"
        self.states = [
            "initial",
            "select",
            "from",
            "where",
            "group_by",
            "having",
            "order_by",
            "final",
        ]
        self.current_state = "initial"
        self.execute_sql = ""
        self.keyword = ["select", "from", "where", "GROUP by", "having", "ORDER by"]
        self.sql_parts = {
            "select": [],
            "from": "",
            "where": [],
            "field": [],
            "value": [],
            "group_by": [],
            "having": [],
            "order_by": [],
        }

    def process_keyword(self, keyword, value=None):
        # 异常返回
        if self.current_state == "select" and keyword not in ["by", "from"]:
            return
        if keyword == "select":
            self.sql_parts["select"].append(value)
            self.current_state = "select"
        elif keyword == "from":
            self.sql_parts["from"] = value
            self.current_state = "from"
        elif keyword == "where":
            self.sql_parts["where"].append(value)
            self.current_state = "where"
        elif keyword == "group_by":
            self.sql_parts["group_by"].append(value)
            self.current_state = "group_by"
        elif keyword == "having":
            self.sql_parts["having"].append(value)
            self.current_state = "having"
        elif keyword == "order_by":
            self.sql_parts["order_by"].append(value)
            self.current_state = "order_by"
        elif keyword == "by":
            self.current_state = "by"
        elif keyword == "insertField":
            self.sql_parts["field"].append(value)
        elif keyword == "insertValue":
            self.sql_parts["value"].append(value)

            pass  # 其他可能的状态处理

    def selectMode(self):
        if self.mode != "select":
            return True
        if not self.sql_parts["select"]:
            self.sql_parts["select"] = ["*"]
        execute_sql = f"select {' ,'.join(self.sql_parts['select'])} from {self.sql_parts['from']} "
        if self.sql_parts["where"]:
            execute_sql += f"where {' AND '.join(self.sql_parts['where'])} "
        if self.sql_parts["group_by"]:
            execute_sql += f"GROUP by {' ,'.join(self.sql_parts['group_by'])} "
        if self.sql_parts["having"]:
            execute_sql += f"having {' AND '.join(self.sql_parts['having'])} "
        if self.sql_parts["order_by"]:
            execute_sql += f"ORDER by {' ,'.join(self.sql_parts['order_by'])} "
        self.execute_sql = execute_sql

    def postMode(self):
        if self.mode != "post":
            return True
        values_str_list = [
            f"({', '.join(map(str, row))})" for row in self.sql_parts["value"]
        ]

        # 合并成一条INSERT语句
        self.execute_sql = f"INSERT INTO {self.sql_parts['from']} ({', '.join(self.sql_parts['field'])}) VALUES {', '.join(values_str_list)};"

    def deleteMode(self):
        if self.mode != "delete":
            return True
        self.execute_sql = f"DELETE from {self.sql_parts['from']} "
        if self.sql_parts["where"]:
            self.execute_sql += f"where {' AND '.join(self.sql_parts['where'])} "

    def updateMode(self):
        if self.mode != "update":
            return True

        data_dict = dict(zip(self.sql_parts["field"], self.sql_parts["value"]))
        set_clause = ", ".join(
            [f"{key} = '{value}'" for key, value in data_dict.items()]
        )
        self.execute_sql = f"UPDATE {self.sql_parts['from']} SET {set_clause}"
        self.execute_sql += f" where {' AND '.join(self.sql_parts['where'])}"

    def finalize(self):
        self.execute_sql = ""

        self.selectMode() and self.postMode() and self.updateMode() and self.deleteMode()

        self.current_state = "final"
        self.sql_parts = {
            "select": [],
            "from": self.sql_parts["from"],
            "where": [],
            "group_by": [],
            "having": [],
            "field": [],
            "value": [],
            "order_by": [],
        }
        return self.execute_sql

T = TypeVar("T", bound="LaModel")

class LaModel(metaclass=ABCMeta):
    def __init_subclass__(self) -> None:
        self.state_machine.process_keyword("from", self.tablename)
        self.getValue = dict().get

    excuteSql = ""
    state_machine = SqlStateMachine()
    cacheSql = {}
    @classmethod
    async def dynamic(
        cls: type[T], dynamicSql: str, params: str | list = None
    ):
        '''
        params是sql参数值
        '''
        if cls.cacheSql.get(dynamicSql):
            return await PPA.exec(sql=cls.cacheSql.get(dynamicSql),params=params,execOne=True)  
        cls.cacheSql[dynamicSql] = cls.state_machine.execute_sql    
       
        if params and not isinstance(params, (list, tuple)):
            params = [params]
         # 翻译dynamicSql    
        cls.parseMethodToSql(dynamicSql)
        res = await cls.exec(params=params,fetch_one=True)    
        return res
    @classmethod
    def parseMethodToSql(cls: type[T],dynamicSql: str):
        # 使用正则表达式找到所有大写字母的位置并进行分割
        parts = re.split("(?=[A-Z])", dynamicSql)
        # 去除可能出现的空字符串（例如：首位是大写字母的情况）
        parts = [part for part in parts if part]
        cls.state_machine.mode = parts[0]
        for i in parts[1:]:
            if i == "In" and len(cls.state_machine.sql_parts["where"]) > 0:
                cls.state_machine.process_keyword(
                    cls.state_machine.current_state, f'{cls.state_machine.sql_parts["where"].pop()} in (?)'
                )
                continue
            if i == "By" or i == "And":
                cls.state_machine.current_state = "where"
                continue
            cls.state_machine.process_keyword(cls.state_machine.current_state, f'{i}=?')
    @classmethod
    def select(cls: type[T], params: str = "*") -> type[T]:
        cls.state_machine.process_keyword("select", params)
        return cls

    @classmethod
    def sql(cls: type[T]):
        return cls.state_machine.finalize()

    @classmethod
    def where(cls: type[T], **kwargs):
        """
        识别参数 key=value 的键值对

        Config.where(name='admin')
        """
        for key, value in kwargs.items():
            cls.state_machine.process_keyword("where", f"{key}={value}")
        return cls

    @classmethod
    def match(cls: type[T], *args):
        """
        用逗号分隔传的方式，必须是偶数，同时能构成正确的键值对顺序

        Config.match('name',larry,'age',18)
        """
        if len(args) % 2 != 0:
            raise ValueError(
                "Invalid argument length. It should contain an even number of elements for key-value pairs."
            )

        # 使用zip将键和值配对，然后通过列表推导式生成条件子句并调用process_keyword方法
        for key, value in zip(*[iter(args)] * 2):
            cls.state_machine.process_keyword("where", f"{key}={value}")
        return cls

    @classmethod
    def valueIn(cls: type[T], *args):
        pass
        return cls

    @classmethod
    def valueNotIn(cls: type[T], *args):
        pass
        return cls

    @classmethod
    async def get(cls: type[T], primaryId: int | str = None) -> T:
        cls.state_machine.mode = "select"
        if primaryId:
            cls.state_machine.process_keyword("where", f"{cls.primaryKey}={primaryId}")
        res = await cls.exec(True)
        if res:
            for key, _ in cls.dictMap.items():
                setattr(cls, key, res.get(key))
        return cls

    @classmethod
    async def getList(cls: type[T], primaryIdList: list[int] | list[str] = None) -> T:
        if primaryIdList:
            cls.state_machine.process_keyword(
                "where", f"{cls.primaryKey} in {primaryIdList}"
            )
        return await cls.exec()

    @classmethod
    async def post(cls: type[T], data: T | list[T] = None):
        cls.state_machine.mode = "post"
        if data and not isinstance(data, (list, tuple)):
            data = [data]

        for key, _ in cls.dictMap.items():
            cls.state_machine.process_keyword("insertField", key)
        for item in data:
            cls.state_machine.process_keyword(
                "insertValue", [getattr(item, key) for key, _ in cls.dictMap.items()]
            )
        return await cls.exec(True)

    @classmethod
    async def update(cls: type[T], data: T | list[T] = None):
        cls.state_machine.mode = "update"
        if data and not isinstance(data, (list, tuple)):
            data = [data]

        for item in data:
            cls.state_machine.process_keyword(
                "where", f"{cls.primaryKey}={getattr(item, cls.primaryKey)}"
            )
            for key, _ in cls.dictMap.items():
                if key == cls.primaryKey:
                    continue
                cls.state_machine.process_keyword("insertField", key)
                cls.state_machine.process_keyword(
                    "insertValue", str(getattr(item, key))
                )
            await cls.exec(True)
        return True

    @classmethod
    async def delete(
        cls: type[T], primaryId: int | str | list[int] | list[str] = None
    ) -> T:
        """
        primaryId参数是对主键进行限制
        """
        cls.state_machine.mode = "delete"

        if primaryId:
            cls.state_machine.process_keyword("where", f"{cls.primaryKey}={primaryId}")
        await cls.exec(True)
        return cls

    @classmethod
    async def exec(cls, fetch_one: bool = False,params={}):
        """
        执行sql fetch_one true是返回单条数据,fetch_many是返回列表数据
        """
        sql = cls.state_machine.finalize()
        if PPA.showMode:
            print(sql)
        res = await PPA.exec(sql, params, fetch_one)
        return res


class FieldDescriptor:
    def __init__(self, primary=False):
        self.primary = primary

    def __set_name__(self, owner, name):
        if not hasattr(owner, "dictMap"):
            owner.dictMap = {}
        owner.dictMap[name] = {}
        owner.dictMap[name]["primary"] = self.primary
        if self.primary:
            owner.primaryKey = name


# 装饰器
def table(_table_name: str = None):
    def wrapper(cls):
        class DecoratedModel(LaModel, cls):
            # 将表名存储到类属性中
            tablename = _table_name if _table_name else cls.__name__.lower()

            def __init_subclass__(cls) -> None:
                # 初始化内容
                return super().__init_subclass__()

        return DecoratedModel

    return wrapper

def sql(func):
   
    sig = inspect.signature(func)
    return_annotation = sig.return_annotation
    def wrapper(*args, **kwargs):
        
        # 获取方法名和参数
        method_name = func.__name__
        method_cache_name = func.__qualname__
        params = [str(arg) for arg in args]
        print(params, method_name,method_cache_name)
          
        # 检查并处理返回类型
        
        print(f"Method '{method_name}' has a return type annotation of: {return_annotation}")

        # 翻译方法成SQL语句
        if method_name == 'selectByAccountAndPassword':
            # 这里模拟根据return_annotation返回对应类型的值,比如列表处理为列表,单个处理单个对象
            # todo 后期优化为从对象内部的局部map获取类定义，然后用反射创建对象

            return params[1:]
        raise ValueError(f"Unsupported SQL operation for method: {method_name}")

    # 转换为类方法并返回
    return classmethod(wrapper)
