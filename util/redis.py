# 配置 Redis
import redis


REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = ""
# 初始化 Redis 客户端
redisTool = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD if REDIS_PASSWORD else None)
