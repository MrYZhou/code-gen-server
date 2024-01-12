import turtle
from typing import Dict, Union
import aiomysql
from fastapi import FastAPI


class PPA:
    _instance = None
    pool = None

    @classmethod
    def init_app(cls, app: FastAPI, **kwargs):
        if cls._instance is None:
            default_values = {
                "host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "password": "root",
                "db": "study",
                "charset": "utf8mb4",
                "autocommit": True,
            }
            kwargs.update(default_values)

            cls._instance = cls()

            # 将更新后的kwargs传递给startup方法以便初始化数据库连接池
            cls.startup_params = kwargs
            app.add_event_handler("startup", cls.startup)
            app.add_event_handler("shutdown", cls.shutdown)

    @classmethod
    async def startup(cls):
        cls.pool = await aiomysql.create_pool(**cls.startup_params)

    @classmethod
    async def shutdown(cls):
        if cls.pool is not None:
            cls.pool.close()
            await cls.pool.wait_closed()

    @classmethod
    async def exec(cls, sql: str, params: Union[Dict[str, any], tuple, list] = None):
        # 校验params中sql参数的合法性
        if params is not None and not isinstance(params, (dict, tuple, list)):
            raise TypeError("params must be a dict, tuple or list")
        # sql注入攻击过滤处理
        sql = sql.replace("?", "%s")
        
        if isinstance(params, (dict)):
            # 参数化查询（使用字典）
            temp_params=tuple(params.values())
            
            sql = sql.format_map(dict.fromkeys(params.keys()))
            # safe_params = [f"{k}" for k in params.keys()]
            # sql = sql.replace( "{".join(safe_params).join("}"),'%s')
            params = temp_params
        elif isinstance(params, (list, tuple)):
            # 参数化查询（使用元组或列表）
            # safe_params = [f"{p}" for p in range(len(params))]
            # sql = sql.replace("?", ", ".join(safe_params))
            pass

        async with cls.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql,params)
                return await cur.fetchall()
