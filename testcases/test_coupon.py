import pytest
import allure
from api.coupon_api import CouponAPI
from testcases.conftest import load_yaml
from utils.extract import Extractor

data = load_yaml("coupon_data.yaml")


@allure.epic("电商商城接口自动化")
@allure.feature("优惠券模块")
class TestCoupon:

    @allure.story("可领取优惠券列表")
    def test_coupon_list(self):
        with allure.step("获取可领取优惠券列表"):
            resp = CouponAPI.get_coupon_list()
            assert resp.status_code == 200
            body = resp.json()
            assert body["code"] == 0

    @allure.story("领取优惠券")
    @pytest.mark.parametrize("case", data["receive_coupon"], ids=[c["case_name"] for c in data["receive_coupon"]])
    def test_receive_coupon(self, case):
        with allure.step(f"用例：{case['case_name']}"):
            resp = CouponAPI.receive_coupon(case["coupon_id"])
            assert resp.status_code == case["expected_status"]
            body = resp.json()
            assert body["code"] == case["expected_code"]
            if case.get("extract_user_coupon"):
                assert Extractor.get("user_coupon_id"), "领取优惠券后未提取到user_coupon_id"

    @allure.story("我的优惠券")
    @pytest.mark.smoke
    def test_my_coupons(self):
        with allure.step("查询未使用优惠券列表"):
            resp = CouponAPI.get_my_coupons(status=0)
            assert resp.status_code == 200
            body = resp.json()
            assert body["code"] == 0
