import jsonpath
from common.logger import logger


class Extractor:
    """
    接口依赖提取器：从响应中提取字段，存入全局缓存，供后续接口使用
    典型场景：登录后取token → 加购取product_id → 下单取order_id → 支付用order_id
    """

    # 全局缓存
    _cache = {}

    @classmethod
    def extract(cls, resp_json, expr, key):
        """
        从响应JSON中提取值并缓存
        :param resp_json: 接口返回的dict
        :param expr: jsonpath表达式，如 $.data.token
        :param key: 缓存键名，如 'token'、'order_id'
        """
        values = jsonpath.jsonpath(resp_json, expr)
        if not values:
            logger.warning(f"jsonpath未匹配到值: {expr}，响应={resp_json}")
            return None
        value = values[0]
        cls._cache[key] = value
        logger.info(f"提取依赖字段 [{key}] = {value}")
        return value

    @classmethod
    def get(cls, key, default=None):
        """从缓存中取值"""
        return cls._cache.get(key, default)

    @classmethod
    def clear(cls):
        """清空缓存（每个测试session开始时调用）"""
        cls._cache.clear()
        logger.info("依赖缓存已清空")
