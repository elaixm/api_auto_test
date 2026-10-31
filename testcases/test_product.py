import pytest
import allure
from api.product_api import ProductAPI
from testcases.conftest import load_yaml

data = load_yaml("product_data.yaml")


@allure.epic("电商商城接口自动化")
@allure.feature("商品模块")
class TestProduct:

    @allure.story("商品列表")
    @pytest.mark.smoke
    @pytest.mark.parametrize("case", data["product_list"], ids=[c["case_name"] for c in data["product_list"]])
    def test_product_list(self, case):
        with allure.step(f"用例：{case['case_name']}"):
            resp = ProductAPI.get_product_list(
                page=case["page"],
                size=case["size"],
                category=case.get("category"),
                keyword=case.get("keyword"),
            )
            assert resp.status_code == case["expected_status"]
            body = resp.json()
            assert body["code"] == case["expected_code"]
            if case.get("expected_list_empty"):
                assert len(body["data"]["list"]) == 0

    @allure.story("商品详情")
    @pytest.mark.parametrize("case", data["product_detail"], ids=[c["case_name"] for c in data["product_detail"]])
    def test_product_detail(self, case):
        with allure.step(f"用例：{case['case_name']}"):
            resp = ProductAPI.get_product_detail(case["product_id"])
            assert resp.status_code == case["expected_status"]
            body = resp.json()
            assert body["code"] == case["expected_code"]
