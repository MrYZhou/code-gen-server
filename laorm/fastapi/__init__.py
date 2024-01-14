from .PPAFastAPI import PPAFastAPI  # 导入PPAFastAPI类

__all__ = ["PPA"]  # 在import * 时候，暴露的东西
PPA = PPAFastAPI  # 设置别名
