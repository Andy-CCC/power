import os
# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ===================== 需自定义的配置 =====================
BASE_URL = "https://fas-api.flextv9.com"  # 替换为你的接口域名
TIMEOUT = 10                        # 请求超时时间
TOKEN = ""                          # 登录Token（有则填）
TOKEN_HEADER = "Authorization"      # Token的请求头Key
IS_SIGN = False                     # 是否开启接口签名（按需开启）
APP_SECRET = "your_secret_key"      # 签名秘钥（开启签名时填）
# ==========================================================

# 默认请求头
DEFAULT_HEADERS = {
    "Content-Type": "application/json;charset=UTF-8"
}