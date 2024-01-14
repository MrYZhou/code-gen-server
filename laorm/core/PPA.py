from typing import Dict, Optional, Union
import aiomysql


class PPA:
    _instance = None
    pool = None
    showSql = True

    @classmethod
    def showSql(cls, show: bool):
        cls.showSql = show

    @classmethod
    async def startup(cls):
        PPA.pool = await aiomysql.create_pool(**cls.startup_params)

    @classmethod
    async def shutdown(cls):
        if cls.pool is not None:
            cls.pool.close()
            await cls.pool.wait_closed()

    @classmethod
    async def exec(
        cls,
        sql: str,
        params: Union[Dict[str, any], tuple, list] = None,
        execOne: Optional[bool] = False,
    ):
        # sql注入攻击过滤处理
        sql = sql.replace("?", "%s")

        if isinstance(params, (dict)):
            # 参数化查询（使用字典）,转元组
            sql = sql.format_map(dict.fromkeys(params.keys(), "%s"))
            params = tuple(params.values())

        async with cls.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql, params)
                return await cur.fetchone() if execOne else await cur.fetchall()
