from common.request import http
from utils.extract import Extractor


class OrderAPI:
    """订单接口封装"""

    @staticmethod
    def create_order(address_id, remark="", coupon_id=None):
        """创建订单，返回order_id供后续接口使用"""
        body = {"address_id": address_id, "remark": remark}
        if coupon_id:
            body["coupon_id"] = coupon_id
        resp = http.post("/api/order/create", json=body)
        # 提取order_id存入缓存
        data = resp.json()
        Extractor.extract(data, "$.data.order_id", "order_id")
        return resp

    @staticmethod
    def get_order_detail(order_id=None):
        """订单详情，默认取缓存中的order_id"""
        oid = order_id or Extractor.get("order_id")
        return http.get(f"/api/order/detail/{oid}")

    @staticmethod
    def get_order_list(page=1, size=10, status=None):
        """订单列表"""
        params = {"page": page, "size": size}
        if status is not None:
            params["status"] = status
        return http.get("/api/order/list", params=params)

    @staticmethod
    def cancel_order(order_id=None):
        """取消订单"""
        oid = order_id or Extractor.get("order_id")
        return http.post(f"/api/order/cancel/{oid}")

    @staticmethod
    def pay_order(order_id=None, pay_method="wechat"):
        """支付订单"""
        oid = order_id or Extractor.get("order_id")
        return http.post("/api/order/pay", json={
            "order_id": oid,
            "pay_method": pay_method,
        })
