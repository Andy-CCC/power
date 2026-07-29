from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# -------- 1. 浏览器配置 --------
chrome_options = Options()
# 如果之前配置了 chrome_options.binary_location，请保留
chrome_options.binary_location = r"D:\chrome-test\chrome-win64\chrome.exe"  # 替换成你的实际路径
# chrome_options.add_argument("--headless")  # 如需后台运行，取消注释
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

try:
    # -------- 2. 打开页面 --------
    print("🚀 正在打开 FlexTV 网页...")
    driver.get("https://www-h5.flextv9.com/")

    # 等待页面加载完成（等待一个关键元素）
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".icon-search")))
    print("✅ 页面加载成功！")

    # -------- 3. 点击搜索按钮（点击搜索图标）--------
    # 优先尝试点击父级按钮或链接，如果没有则直接点击图标
    try:
        # 尝试点击包含搜索图标的父级元素
        search_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-btn, [class*='search'] button, a[class*='search']")))
        search_btn.click()
        print("🔍 已点击搜索按钮（父级元素）")
    except:
        # 如果上面的方法找不到，直接点击图标本身
        search_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".icon-search")))
        search_icon.click()
        print("🔍 已点击搜索按钮（图标元素）")

    # 等待搜索框出现
    time.sleep(1)

    # -------- 4. 点击输入框（聚焦输入框）--------
    try:
        # 定位搜索输入框
        search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                              "input[type='search'], input[type='text'], input[placeholder*='搜索'], input[placeholder*='Search']")))
        search_input.click()  # 点击输入框使其获得焦点
        print("🖱️ 已点击搜索输入框")
    except Exception as e:
        print(f"⚠️ 点击输入框失败: {e}")
        # 尝试更通用的定位方式
        search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input")))
        search_input.click()
        print("🖱️ 已点击搜索输入框（使用备选定位）")

    # 清空输入框（以防有默认文字）
    search_input.clear()

    # -------- 5. 输入内容 --------
    search_keyword = "我是刘邦"
    search_input.send_keys(search_keyword)
    print(f"📝 已输入内容: {search_keyword}")

    # 等待一下，让输入生效
    time.sleep(0.5)

    # -------- 6. 按回车键搜索 --------
    search_input.send_keys(Keys.RETURN)
    print("✅ 已按回车键，开始搜索")

    # 等待搜索结果加载
    time.sleep(3)

    # 验证搜索是否成功（可选）
    try:
        # 等待搜索结果中出现内容
        wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, search_keyword)))
        print(f"🎉 搜索成功！页面包含关键词: {search_keyword}")
    except:
        print("⚠️ 搜索结果页面未包含预期关键词，请检查")

    # 保存截图用于调试
    driver.save_screenshot("search_result.png")
    print("📸 搜索结果截图已保存为 search_result.png")

except Exception as e:
    print(f"❌ 自动化过程中出现错误: {e}")
    driver.save_screenshot("error_screenshot.png")
    print("📸 错误截图已保存为 error_screenshot.png")

finally:
    # 等待几秒让你观察结果（调试用）
    time.sleep(3)
    driver.quit()
    print("🔚 浏览器已关闭")