from common.request import http
from utils.extract import Extractor


class CouponAPI:
    """优惠券接口封装"""

    @staticmethod
    def get_coupon_list():
        """可领取优惠券列表"""
        return http.get("/api/coupon/list")

    @staticmethod
    def receive_coupon(coupon_id):
        """领取优惠券，提取用户优惠券ID"""
        resp = http.post("/api/coupon/receive", json={"coupon_id": coupon_id})
        data = resp.json()
        Extractor.extract(data, "$.data.user_coupon_id", "user_coupon_id")
        return resp

    @staticmethod
    def get_my_coupons(status=0):
        """我的优惠券列表，status: 0未使用 1已使用 2已过期"""
        return http.get("/api/coupon/my", params={"status": status})
