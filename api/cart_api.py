from common.request import http
from utils.extract import Extractor


class CartAPI:
    """购物车接口封装"""

    @staticmethod
    def add_to_cart(product_id, quantity=1):
        """加入购物车"""
        return http.post("/api/cart/save", json={
            "product_id": product_id,
            "quantity": quantity,
        })

    @staticmethod
    def get_cart_list():
        """商品收藏列表"""
        return http.get("/api/usergoodsfavor/index")

    @staticmethod
    def update_cart_item(item_id, quantity):
        """修改购物车商品数量"""
        return http.put("/api/cart/update", json={
            "item_id": item_id,
            "quantity": quantity,
        })

    @staticmethod
    def delete_cart_item(item_id):
        """删除购物车商品"""
        return http.delete(f"/api/cart/item/{item_id}")

    @staticmethod
    def clear_cart():
        """清空购物车"""
        return http.delete("/api/cart/clear")

    @staticmethod
    def buy_cart():
        """订单确认"""
        return http.post("/api/buy/index")
