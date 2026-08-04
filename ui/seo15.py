from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# 浏览器配置
chrome_options = Options()
chrome_options.binary_location = r"D:\chrome-test\chrome-win64\chrome.exe"
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=chrome_options)
# 等待对象
wait = WebDriverWait(driver, 12)
short_wait = WebDriverWait(driver, 3)

try:
    # 1. 打开网站
    url = "https://www-h5.flextv9.com/"
    print("【步骤1】打开FlexTV网页")
    driver.get(url)
    time.sleep(1)

    # 2. 定位左上角FlexTV Logo图片
    print("【步骤2】定位左上角FlexTV logo按钮")
    logo_locator = (By.CSS_SELECTOR, "img.logo")
    # 断言1：logo元素可点击
    logo_elem = wait.until(EC.element_to_be_clickable(logo_locator))
    print("✅ 断言通过：FlexTV logo按钮存在且可点击")

    # 3. 点击logo（JS点击，解决页面切换动画导致点击失效）
    print("【步骤3】点击左上角FlexTV按钮返回首页")
    driver.execute_script("arguments[0].click();", logo_elem)
    time.sleep(1)

    # 4. 后置断言：点击后成功回到首页，首页搜索图标可见
    print("【步骤4】校验是否成功返回首页")
    search_icon_locator = (By.CSS_SELECTOR, ".icon-search")
    #逻辑：持续轮询页面，直到元素**DOM 存在 + 页面肉眼可见**；超时直接抛异常，用例失败
    short_wait.until(EC.visibility_of_element_located(search_icon_locator))
    print("✅ 断言通过：点击logo后正常回到首页，搜索图标可见")

    print("\n🎉 全部操作与断言执行成功！")

except Exception as err:
    print(f"\n❌ 执行失败，错误信息：{str(err)}")
    # 失败截图留存证据
    driver.save_screenshot("logo_click_error.png")
    print("已保存失败截图：logo_click_error.png")

finally:
    time.sleep(5)
    driver.quit()
    print("\n浏览器关闭")
