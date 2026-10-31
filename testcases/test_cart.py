import pytest
import allure
from api.cart_api import CartAPI
from testcases.conftest import load_yaml

data = load_yaml("cart_data.yaml")


@allure.epic("电商商城接口自动化")
@allure.feature("购物车模块")
class TestCart:

    @allure.story("加入购物车")
    @pytest.mark.parametrize("case", data["add_to_cart"], ids=[c["case_name"] for c in data["add_to_cart"]])
    def test_add_to_cart(self, case):
        with allure.step(f"用例：{case['case_name']}"):
            resp = CartAPI.add_to_cart(case["product_id"], case["quantity"])
            assert resp.status_code == case["expected_status"]
            body = resp.json()
            assert body["code"] == case["expected_code"]

    @allure.story("购物车列表")
    @pytest.mark.smoke
    def test_get_cart_list(self):
        with allure.step("获取购物车列表"):
            resp = CartAPI.get_cart_list()
            assert resp.status_code == 200
            body = resp.json()
            assert body["code"] == 0

    @allure.story("清空购物车")
    def test_clear_cart(self):
        with allure.step("清空购物车"):
            resp = CartAPI.clear_cart()
            assert resp.status_code == 200
            body = resp.json()
            assert body["code"] == 0
