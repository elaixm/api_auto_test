from common.request import http
from utils.extract import Extractor


class ProductAPI:
    """商品相关接口封装"""

    @staticmethod
    def get_product_list(page=1, size=10, category=None, keyword=None):
        """商品列表"""
        params = {"page": page, "size": size}
        if category:
            params["category"] = category
        if keyword:
            params["keyword"] = keyword
        return http.get("/api/product/list", params=params)

    @staticmethod
    def get_product_detail(product_id):
        """商品详情"""
        return http.get(f"/api/product/detail/{product_id}")

    @staticmethod
    def get_hot_products():
        """热门商品"""
        return http.get("/api/product/hot")
