from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time

# ==========================
# 浏览器配置
# ==========================

chrome_options = Options()
chrome_options.binary_location = r"D:\chrome-test\chrome-win64\chrome.exe"

driver = webdriver.Chrome(options=chrome_options)

driver.maximize_window()

wait = WebDriverWait(driver, 15)

HOME_URL = "https://www.flextv.cc"

TOTAL_COUNT = 100

ad_count = 0

no_ad_count = 0


def has_ad():
    """
    判断广告是否存在
    """
    try:

        WebDriverWait(driver, 5).until(

            EC.visibility_of_element_located(

                (
                    By.CSS_SELECTOR,
                    "div.google-adsense-banner.adsense-banner--pc"
                )

            )

        )

        return True

    except TimeoutException:

        return False


for i in range(1, TOTAL_COUNT + 1):

    print("=" * 60)

    print(f"开始第 {i} 次测试")

    # 打开首页
    driver.get(HOME_URL)

    # 等待Banner
    banner = wait.until(

        EC.element_to_be_clickable(

            (
                By.CSS_SELECTOR,
                ".hero-section h3 a"
            )

        )

    )

    # 点击Banner
    banner.click()

    # 等待播放页加载
    wait.until(

        EC.presence_of_element_located(

            (
                By.CSS_SELECTOR,
                ".play.pc_container"
            )

        )

    )

    # 等2秒给广告加载
    time.sleep(2)

    # 判断广告
    if has_ad():

        ad_count += 1

        print(f"第{i}次：✅ 出现广告")

    else:

        no_ad_count += 1

        print(f"第{i}次：❌ 未出现广告")


print("\n")

print("=" * 60)

print("测试结束")

print(f"总次数：{TOTAL_COUNT}")

print(f"广告出现次数：{ad_count}")

print(f"未出现次数：{no_ad_count}")

print(f"广告出现率：{ad_count / TOTAL_COUNT:.2%}")

driver.quit()