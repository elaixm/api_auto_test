from common.request import http
from utils.extract import Extractor


class UserAPI:
    """用户相关接口封装"""

    @staticmethod
    def login(username, password):
        """登录，返回响应，并自动提取token存入缓存"""
        resp = http.post("/api/user/login", json={
            "username": username,
            "password": password,
        })
        # 提取token，后续所有接口自动携带
        data = resp.json()
        Extractor.extract(data, "$.data.token", "token")
        http.set_token(Extractor.get("token"))
        return resp

    @staticmethod
    def get_user_info():
        """获取当前用户信息"""
        return http.get("/api/user/info")

    @staticmethod
    def register(username, password, email=""):

        """注册"""
        return http.post("/api/user/register", json={
            "username": username,
            "password": password,
            "email": email,
        })

    @staticmethod
    def update_user_info(nickname=None, avatar=None):
        """修改用户信息"""
        body = {}
        if nickname:
            body["nickname"] = nickname
        if avatar:
            body["avatar"] = avatar
        return http.put("/api/user/info", json=body)
