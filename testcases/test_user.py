import pytest
import allure
from api.user_api import UserAPI
from testcases.conftest import load_yaml
from config.settings import config

data = load_yaml("user_data.yaml")


@allure.epic("电商商城接口自动化")
@allure.feature("用户模块")
class TestUser:

    @allure.story("登录")
    @pytest.mark.parametrize("case", data["login_success"], ids=[c["case_name"] for c in data["login_success"]])
    def test_login_success(self, case):
        with allure.step(f"用例：{case['case_name']}"):
            resp = UserAPI.login(case["username"], case["password"])
            assert resp.status_code == case["expected_status"]
            body = resp.json()
            assert body["code"] == case["expected_code"]

    @allure.story("登录失败")
    @pytest.mark.negative
    @pytest.mark.parametrize("case", data["login_fail"], ids=[c["case_name"] for c in data["login_fail"]])
    def test_login_fail(self, case):
        with allure.step(f"用例：{case['case_name']}"):
            resp = UserAPI.login(case["username"], case["password"])
            assert resp.status_code == case["expected_status"]
            body = resp.json()
            assert body["code"] == case["expected_code"]
            assert case["expected_msg"] in body.get("message", "")

    @allure.story("获取用户信息")
    @pytest.mark.smoke
    def test_get_user_info(self):
        with allure.step("获取当前登录用户信息"):
            resp = UserAPI.get_user_info()
            assert resp.status_code == 200
            body = resp.json()
            assert body["code"] == 0
            assert "data" in body

    @allure.story("注册")
    @pytest.mark.negative
    @pytest.mark.parametrize("case", data["register"], ids=[c["case_name"] for c in data["register"]])
    def test_register(self, case):
        with allure.step(f"用例：{case['case_name']}"):
            resp = UserAPI.register(case["username"], case["password"], case.get("email", ""))
            assert resp.status_code == case["expected_status"]
            body = resp.json()
            assert body["code"] == case["expected_code"]
