import os
# 项目根目录（无需改）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ===================== 需修改的配置（必改） =====================
# 1. 接口域名（选对应环境，注释掉不用的）
TEST_ENV = "测试环境"
BASE_URL = "https://fas-api.flextv9.com"  # 公司测试环境域名
# TEST_ENV = "预发布环境"
# BASE_URL = "http://pre.api.xxx.com"     # 公司预发布环境域名
# TEST_ENV = "生产环境（谨慎）"
# BASE_URL = "http://prod.api.xxx.com"

# 2. 登录配置（获取Token）
LOGIN_URL = "/admin/member/login"        # 公司登录接口路径
LOGIN_PARAMS = {                       # 登录请求参数（JSON格式）
    "username": "18218410011",               # 替换为公司真实账号
    "password": "8888"               # 替换为公司真实密码
}
TOKEN_HEADER = "Authorization"         # Token请求头（如Bearer Token/Token）
TOKEN_PREFIX = "Bearer "               # Token前缀（无则留空，例：Bearer eyJhbGciOiJIUzI1NiJ9）

# 3. 基础配置
TIMEOUT = 10                           # 请求超时时间（秒）
LOG_LEVEL = "INFO"                     # 日志级别（INFO/DEBUG/ERROR）
# ===============================================================

# 固定配置（无需改）
DEFAULT_HEADERS = {
    "Content-Type": "application/json;charset=UTF-8"
}