# 导入网络请求库（最核心的爬虫库）
import requests
from bs4 import BeautifulSoup

# 1. 定义要爬取的网址（这里用百度首页测试）
url = "https://www.baidu.com"

try:
    # 2. 发送HTTP GET请求（和浏览器访问网页原理一样）
    response = requests.get(url, timeout=10)
    # 3. 检查请求是否成功（状态码200=成功）
    response.raise_for_status()
    # 4. 设置正确编码（防止中文乱码）
    response.encoding = "utf-8"

    # 5. 打印结果
    print("=== 爬取成功 ===")
    print(f"状态码：{response.status_code}")
    print(f"网页标题所在位置（HTML）：{response.text[:500]}...")  # 只打印前500字符避免太长

except Exception as e:
    print(f"爬取失败：{e}")
# 新增：解析HTML提取标题（需要安装：pip install beautifulsoup4）


# 解析网页
soup = BeautifulSoup(response.text, "html.parser")
title = soup.title.string  # 提取标题

print(f"\n网页标题：{title}")