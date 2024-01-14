from typing import TypeVar
from abc import ABCMeta
from laorm.fastapi import PPA


class SqlStateMachine:
    def __init__(self, *args):
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
            "group_by": [],
            "having": [],
            "order_by": [],
        }

    def process_keyword(self, keyword, value=None):
        keyword = keyword.upper()
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
            # self.sql_parts['order_by'].append(value)
            self.current_state = "BY"
            pass  # 其他可能的状态处理

    def finalize(self):
        self.execute_sql = ""
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

        self.execute_sql = execute_sql
        self.current_state = "FINAL"
        self.sql_parts = {
            "select": [],
            "from": self.sql_parts["from"],
            "where": [],
            "group_by": [],
            "having": [],
            "order_by": [],
        }
        return self.execute_sql


T = TypeVar("T", bound="LaModel")


class LaModel(metaclass=ABCMeta):
    def __init_subclass__(self) -> None:
        self.state_machine.process_keyword("FROM", self.tablename)

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
    def where(cls: type[T], *args):
        if len(args) % 2 != 0:
            raise ValueError(
                "Invalid argument length. It should contain an even number of elements for key-value pairs."
            )

        # 使用zip将键和值配对，然后通过列表推导式生成条件子句并调用process_keyword方法
        for key, value in zip(*[iter(args)] * 2):
            cls.state_machine.process_keyword("WHERE", f"{key}={value}")
        return cls

    @classmethod
    def match(cls: type[T], *args):
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

    # 结束方法,需要进行sql的构建,执行
    @classmethod
    async def get(cls: type[T], primaryId: int | str):
        if primaryId:
            cls.state_machine.process_keyword("WHERE", f"{cls.primaryKey}={primaryId}")
        return await cls.exec(True)

    @classmethod
    async def exec(cls, fetch_one: bool):
        sql = cls.state_machine.finalize()
        if PPA.showSql:
            print(sql)
        res = await PPA.exec(sql, {}, fetch_one)
        return res

    @classmethod
    def getList(cls: type[T], primaryIdList: list[int] | list[str]):
        if primaryIdList:
            cls.state_machine.process_keyword(
                "WHERE", f"{cls.primaryKey} in {primaryIdList}"
            )
        cls.exec()


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
