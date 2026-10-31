import yaml
import os


class Config:
    """读取config.yaml配置，支持多环境切换"""

    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        with open(config_path, "r", encoding="utf-8") as f:
            self._cfg = yaml.safe_load(f)

        # 通过环境变量切换环境，默认 test
        self.env = os.getenv("ENV", self._cfg.get("active_env", "test"))
        self._env_cfg = self._cfg[self.env]

    @property
    def base_url(self):
        return self._env_cfg["base_url"]

    @property
    def timeout(self):
        return self._env_cfg.get("timeout", 10)

    def get_account(self, role="normal_user"):
        return self._env_cfg[role]


config = Config()
