from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import time
from datetime import datetime


# ============================================
# 日志函数
# ============================================

def log_step(message, start_time=None):
    current_time = time.time()

    timestamp = datetime.now().strftime("%H:%M:%S")

    if start_time:
        elapsed = current_time - start_time
        print(
            f"[{timestamp}] {message} (耗时:{elapsed:.2f}秒)"
        )
    else:
        print(
            f"[{timestamp}] {message}"
        )

    return current_time

# ============================================
# 浏览器配置
# ============================================

chrome_options = Options()
# 你的 Chrome 路径
chrome_options.binary_location = (
    r"D:\chrome-test\chrome-win64\chrome.exe")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver,15)
# 记录开始时间
script_start_time = time.time()
try:

    # ============================================
    # 1. 打开网站
    # ============================================
    step_start = log_step("🚀 正在打开 FlexTV...")
    driver.get("https://www-h5.flextv9.com/")
    # 等待语言按钮出现
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".language_val")))
    log_step("✅ 页面加载成功",step_start)
    # ============================================
    # 2. 测试语言切换
    # ============================================
    step_start = log_step("🌍 开始测试所有语言")
    actions = ActionChains(driver)
    language_list = [
        "日本語",
        "English",
        "한국어",
        "ภาษาไทย",
        "Bahasa Indonesia",
        "Español",
        "Français",
        "Deutsch",
        "Português",
        "Italiano",
        "العربية",
        "Türkçe",
        "Русский",
        "繁体中文",
        "简体中文",
        "Tiếng Việt"
    ]
    for language in language_list:
        try:
            # ------------------------------------
            # 重新定位语言入口
            # ------------------------------------
            language_btn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,".language_val")))
            # ------------------------------------
            # 鼠标悬停
            # ------------------------------------
            actions.move_to_element(language_btn).perform()

            log_step("🖱️ 已打开语言菜单")
            # ------------------------------------
            # 等待菜单出现
            # ------------------------------------
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,".language_ul")))
            items = driver.find_elements(By.CSS_SELECTOR,".language_ul li")
            print("当前语言数量：", len(items))
            for item in items:
                print(item.text)
            # ------------------------------------
            # 点击目标语言
            # ------------------------------------
            language_item = wait.until(
                EC.element_to_be_clickable((By.XPATH,f"//ul[@class='language_ul']/li[text()='{language}']")))
            # JS点击，避免遮挡
            driver.execute_script("arguments[0].click();",language_item)
            log_step(f"✅ 已点击语言：{language}")
            # 等待页面语言刷新
            time.sleep(2)
        except Exception as e:
            log_step(
                f"❌ {language} 点击失败:{e}"
            )
    log_step("🎉 所有语言测试完成",step_start)
    # 截图
    driver.save_screenshot("language_test_result.png")
    log_step("📸 已保存截图 language_test_result.png")
except Exception as e:
    error_time = datetime.now().strftime("%H:%M:%S")
    print(f"❌ [{error_time}] 执行失败:{e}")
    driver.save_screenshot("error_language.png")
    print("📸 已保存错误截图")
finally:
    time.sleep(2)
    driver.quit()
    print("🔚 浏览器关闭")
    print(f"脚本总耗时:{time.time() - script_start_time:.2f}秒")
