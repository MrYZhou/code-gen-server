from typing import TypeVar
from abc import ABCMeta
from laorm.core.PPA import PPA
import builtins


class SqlStateMachine:
    def __init__(self, *args):
        self.mode = 'select'
        self.states = [
            "INITIAL",
            "SELECT",
            "FROM",
            "WHERE",
            "GROUP_BY",
            "HAVING",
            "ORDER_BY",
            "FINAL",
        ]
        self.current_state = "INITIAL"
        self.execute_sql = ""
        self.keyword = ["SELECT", "FROM", "WHERE", "GROUP BY", "HAVING", "ORDER BY"]
        self.sql_parts = {
            "select": [],
            "from": "",
            "where": [],
            "field":[],
            "value": [],
            "group_by": [],
            "having": [],
            "order_by": [],
        }

    def process_keyword(self, keyword, value=None):
        # 异常返回
        if self.current_state == "SELECT" and keyword not in ["BY", "FROM"]:
            return
        if keyword == "SELECT":
            self.sql_parts["select"].append(value)
            self.current_state = "SELECT"
        elif keyword == "FROM":
            self.sql_parts["from"] = value
            self.current_state = "FROM"
        elif keyword == "WHERE":
            self.sql_parts["where"].append(value)
            self.current_state = "WHERE"
        elif keyword == "GROUP_BY":
            self.sql_parts["group_by"].append(value)
            self.current_state = "GROUP_BY"
        elif keyword == "HAVING":
            self.sql_parts["having"].append(value)
            self.current_state = "HAVING"
        elif keyword == "ORDER_BY":
            self.sql_parts["order_by"].append(value)
            self.current_state = "ORDER_BY"
        elif keyword == "BY":
            self.current_state = "BY"
        elif keyword == "insertField":
            self.sql_parts["field"].append(value)
        elif keyword == "insertValue":
            self.sql_parts["value"].append(value)     
              
            pass  # 其他可能的状态处理
    def selectMode(self):
        if not self.sql_parts["select"]:
            self.sql_parts["select"] = ["*"]
        execute_sql = f"SELECT {' ,'.join(self.sql_parts['select'])} FROM {self.sql_parts['from']} "
        if self.sql_parts["where"]:
            execute_sql += f"WHERE {' AND '.join(self.sql_parts['where'])} "
        if self.sql_parts["group_by"]:
            execute_sql += f"GROUP BY {' ,'.join(self.sql_parts['group_by'])} "
        if self.sql_parts["having"]:
            execute_sql += f"HAVING {' AND '.join(self.sql_parts['having'])} "
        if self.sql_parts["order_by"]:
            execute_sql += f"ORDER BY {' ,'.join(self.sql_parts['order_by'])} "
        return execute_sql    
    def postMode(self):
        # 将数据转换为所需的字符串格式
        values_str_list = [f"({', '.join(map(str, row))})" for row in self.sql_parts['value']]

        # 合并成一条INSERT语句
        execute_sql = f"INSERT INTO {self.sql_parts['from']} ({', '.join(self.sql_parts['field'])}) VALUES {', '.join(values_str_list)};"

        return execute_sql
    def deleteMode(self):
        execute_sql = f"DELETE FROM {self.sql_parts['from']} "
        if self.sql_parts["where"]:
            execute_sql += f"WHERE {' AND '.join(self.sql_parts['where'])} "       
        return execute_sql    
    def updateMode(self):
        execute_sql = f"update {self.sql_parts['from']} "
        return execute_sql
    def finalize(self):
        self.execute_sql = ""
        if self.mode == 'select':
            self.execute_sql = self.selectMode()
        elif self.mode == 'post':
            self.execute_sql = self.postMode()       
        elif self.mode == 'delete':
            self.execute_sql = self.deleteMode()
        elif self.mode == 'update':
            self.execute_sql = self.updateMode()         
    
        self.current_state = "FINAL"
        self.sql_parts = {
            "select": [],
            "from": self.sql_parts["from"],
            "where": [],
            "group_by": [],
            "having": [],
            "field":[],
            "value":[],
            "order_by": [],
        }
        return self.execute_sql


T = TypeVar("T", bound="LaModel")
# 元类装饰器实现
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


class LaModel(metaclass=ABCMeta):
    def __init_subclass__(self) -> None:
        self.state_machine.process_keyword("FROM", self.tablename)
        self.getValue = dict().get

    excuteSql = ""
    state_machine = SqlStateMachine()
    
    @classmethod
    def select(cls: type[T], params: str = "*") -> type[T]:
        cls.state_machine.process_keyword("SELECT", params)
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
            cls.state_machine.process_keyword("WHERE", f"{key}={value}")
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
            cls.state_machine.process_keyword("WHERE", f"{key}={value}")
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
    async def get(cls: type[T], primaryId: int | str = None)->T:
        cls.state_machine.mode = 'select'
        if primaryId:
            cls.state_machine.process_keyword("WHERE", f"{cls.primaryKey}={primaryId}")
        res= await cls.exec(True)
        if res:
            for key, _ in cls.dictMap.items():
                setattr(cls, key, res.get(key))
        return cls
    @classmethod
    async def getList(cls: type[T], primaryIdList: list[int] | list[str] = None)->T:
        if primaryIdList:
            cls.state_machine.process_keyword(
                "WHERE", f"{cls.primaryKey} in {primaryIdList}"
            )
        return await cls.exec()
    @classmethod
    async def post(cls: type[T], data: T | list[T] = None):
        cls.state_machine.mode = 'post'
        if data and not isinstance(data, (list, tuple)):
            data = [data]
        
        for key, _ in cls.dictMap.items():
            cls.state_machine.process_keyword("insertField",key)    
        for item in data:
            cls.state_machine.process_keyword("insertValue",[getattr(item,key) for  key, _ in cls.dictMap.items()])
        return await cls.exec(True) 
    
    @classmethod
    async def update(cls: type[T], data: T | list[T] = None):
        cls.state_machine.mode = 'update'
        if data.get(cls.primaryKey):
            cls.state_machine.process_keyword("WHERE", f"{cls.primaryKey}={data.get(cls.primaryKey)}")
        await cls.exec(True)
        return cls
    
    @classmethod
    async def delete(cls: type[T], primaryId: int | str | list[int] | list[str]  = None)->T:
        """
        primaryId参数是对主键进行限制
        """
        cls.state_machine.mode = 'delete'

        if primaryId:
            cls.state_machine.process_keyword("WHERE", f"{cls.primaryKey}={primaryId}")
        await cls.exec(True)
        return cls
    
    
    @classmethod
    async def exec(cls, fetch_one: bool = False):
        """
        执行sql fetch_one true是返回单条数据,fetch_many是返回列表数据
        """
        sql = cls.state_machine.finalize()
        if PPA.showMode:
            print(sql)
        res = await PPA.exec(sql, {}, fetch_one)
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




