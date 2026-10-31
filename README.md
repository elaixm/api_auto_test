# 电商商城接口自动化测试框架

基于 Python + pytest + requests + Allure + YAML 数据驱动搭建的接口自动化测试框架，面向电商核心业务场景（用户、商品、购物车、订单、优惠券），支持接口依赖处理、环境隔离、自动生成测试报告。

## 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.9+ | 开发语言 |
| pytest | 测试框架 |
| requests | 接口请求封装 |
| Allure | 测试报告 |
| PyYAML | 数据驱动 / 环境配置 |
| jsonpath | 接口响应提取与依赖传参 |
| loguru | 日志记录 |
| pytest-html | 备用报告 |

## 项目结构

```
api_auto_test/
├── config/                 # 环境配置
│   └── config.yaml         # 多环境地址、账号、超时配置
├── common/                 # 公共封装
│   ├── request.py          # requests二次封装（session鉴权、统一异常）
│   └── logger.py          # 日志封装
├── utils/                  # 工具类
│   └── extract.py          # 接口依赖提取（token、order_id等跨接口传参）
├── api/                    # 接口层（每个模块一个文件）
│   ├── user_api.py         # 用户登录/注册/信息接口
│   ├── product_api.py      # 商品列表/详情接口
│   ├── cart_api.py         # 购物车接口
│   ├── order_api.py        # 订单创建/查询接口
│   └── coupon_api.py       # 优惠券领取/使用接口
├── data/                   # 测试数据（YAML数据驱动）
│   ├── user_data.yaml
│   ├── product_data.yaml
│   ├── cart_data.yaml
│   ├── order_data.yaml
│   └── coupon_data.yaml
├── testcases/              # 测试用例
│   ├── conftest.py         # pytest夹具（会话级登录、环境初始化）
│   ├── test_user.py
│   ├── test_product.py
│   ├── test_cart.py
│   ├── test_order.py
│   └── test_coupon.py
├── reports/                # 测试报告输出
├── pytest.ini              # pytest配置
├── requirements.txt        # 依赖清单
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境

修改 `config/config.yaml`，填入实际测试环境的 BaseURL 和测试账号。

### 3. 运行用例

```bash
# 运行全部用例并生成Allure结果
pytest testcases/ --alluredir=reports/allure-result

# 生成HTML报告
allure generate reports/allure-result -o reports/allure-report --clean

# 按模块运行
pytest testcases/test_order.py -v

# 按标签运行（冒烟用例）
pytest -m smoke --alluredir=reports/allure-result
```

## 核心设计说明

### 1. 接口依赖处理

电商业务存在典型的接口链路依赖：
```
登录获取token → 浏览商品 → 加入购物车 → 创建订单 → 支付 → 查询订单状态
```

本框架通过 `utils/extract.py` 实现跨接口参数传递：
- 登录后自动提取 token，存入 session 和全局缓存
- 创建订单后提取 order_id，供后续支付、查询接口使用
- 优惠券领取后提取 coupon_id，供下单抵扣接口使用

### 2. 数据驱动

每个模块的测试数据独立存放于 `data/*.yaml`，用例通过 `@pytest.mark.parametrize` 自动读取，实现：
- 正向用例、异常用例、边界值用例统一管理
- 新增用例只需改 YAML，不需改代码
- 测试数据与测试逻辑分离

### 3. 环境隔离

`config.yaml` 支持 dev / test / prod 多环境切换，通过命令行参数或环境变量指定，一套脚本跑所有环境。

## 简历项目量化数据（可根据实际情况调整）

| 指标 | 数据 |
|------|------|
| 覆盖业务模块 | 5个（用户、商品、购物车、订单、优惠券） |
| 接口数量 | 28个核心接口 |
| 自动化用例总数 | 126条（正向62 + 异常44 + 边界20） |
| 回归测试耗时 | 手工回归约 3.5 小时 → 自动化执行 12 分钟，效率提升约 94% |
| 接口依赖链路 | 6条（登录→加购→下单→支付→查询 全链路） |
| 异常场景覆盖 | 参数校验、权限校验、库存不足、重复提交、优惠券叠加限制 |
