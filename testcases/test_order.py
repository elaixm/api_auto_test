import pytest
import allure
from api.order_api import OrderAPI
from api.cart_api import CartAPI
from api.product_api import ProductAPI
from testcases.conftest import load_yaml
from utils.extract import Extractor

data = load_yaml("order_data.yaml")


@allure.epic("电商商城接口自动化")
@allure.feature("订单模块")
class TestOrder:

    @allure.story("创建订单")
    @pytest.mark.smoke
    @pytest.mark.parametrize("case", data["create_order"], ids=[c["case_name"] for c in data["create_order"]])
    def test_create_order(self, case):
        with allure.step(f"用例：{case['case_name']}"):
            # 前置：确保购物车有商品
            CartAPI.add_to_cart(10001, 1)
            # 调用创建订单
            coupon_id = None
            if case.get("use_coupon"):
                coupon_id = Extractor.get("user_coupon_id")
            resp = OrderAPI.create_order(
                address_id=case["address_id"],
                remark=case.get("remark", ""),
                coupon_id=coupon_id,
            )
            assert resp.status_code == case["expected_status"]
            body = resp.json()
            assert body["code"] == case["expected_code"]
            # 如果是成功用例，验证order_id被提取
            if case.get("extract_order_id"):
                assert Extractor.get("order_id"), "创建订单后未提取到order_id"

    @allure.story("订单详情")
    @pytest.mark.dependency(depends=["TestOrder::test_create_order"])
    def test_order_detail(self):
        """依赖创建订单用例，使用缓存中的order_id查询"""
        with allure.step("查询刚创建的订单详情"):
            order_id = Extractor.get("order_id")
            pytest.assume(order_id, "前置未生成order_id")
            resp = OrderAPI.get_order_detail(order_id)
            assert resp.status_code == 200
            body = resp.json()
            assert body["code"] == 0
            assert body["data"]["order_id"] == order_id

    @allure.story("订单列表")
    def test_order_list(self):
        with allure.step("查询订单列表"):
            resp = OrderAPI.get_order_list(page=1, size=10)
            assert resp.status_code == 200
            body = resp.json()
            assert body["code"] == 0

    @allure.story("取消订单")
    @pytest.mark.negative
    def test_cancel_order(self):
        with allure.step("创建订单后取消"):
            CartAPI.add_to_cart(10001, 1)
            create_resp = OrderAPI.create_order(address_id=1)
            order_id = create_resp.json()["data"]["order_id"]
            cancel_resp = OrderAPI.cancel_order(order_id)
            assert cancel_resp.status_code == 200
            body = cancel_resp.json()
            assert body["code"] == 0
