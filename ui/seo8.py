from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime

def log_step(message, start_time=None):
    current_time = time.time()
    timestamp = datetime.now().strftime("%H:%M:%S")
    if start_time:
        elapsed = current_time - start_time
        print(f"[{timestamp}] {message} (耗时:{elapsed:.2f}秒)")
    else:
        print(f"[{timestamp}] {message}")
    return current_time

# 浏览器配置
chrome_options = Options()
chrome_options.binary_location = r"D:\chrome-test\chrome-win64\chrome.exe"
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--start-maximized")
# 提速参数
chrome_options.add_argument("--disable-images")  # 可选：关闭图片加载大幅提速，不需要删掉此行
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 12)
short_wait = WebDriverWait(driver, 3)  # 缩短短时等待
script_start_time = time.time()

try:
    step_start = log_step("🚀 正在打开 FlexTV...")
    driver.get("https://www-h5.flextv9.com/")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".language_val")))
    # 【优化】不再固定sleep(2)，轮询等待页面就绪，超时兜底
    wait.until(lambda d: d.execute_script("return document.readyState === 'complete'"))
    log_step("✅ 页面资源加载完成", step_start)

    step_start = log_step("🌍 开始测试所有语言")
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
            language_btn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".language_val")))
            dropdown_success = False
            retry_times = 0

            while retry_times < 3 and not dropdown_success:
                try:
                    # 【提速】pause由1s → 0.4s
                    ActionChains(driver).move_to_element(language_btn).pause(0.4).perform()
                    driver.execute_script("""
                        const target = arguments[0];
                        target.dispatchEvent(new MouseEvent('mouseover', {bubbles:true}));
                    """, language_btn)
                    # 缩短悬浮后等待
                    short_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".language_ul")))
                    dropdown_success = True
                    log_step("✅ 语言下拉菜单成功展开")
                except Exception:
                    retry_times += 1
                    log_step(f"⚠️ 下拉菜单展开失败，重试第{retry_times}次")
                    ActionChains(driver).move_by_offset(-200, 0).pause(0.2).perform()

            if not dropdown_success:
                raise Exception("多次重试仍然无法弹出语言下拉菜单")

            items = short_wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".language_ul li")))
            print(f"[{language}] 当前语言下拉数量：", len(items))

            target_xpath = f"//ul[@class='language_ul']/li[normalize-space(.)='{language}']"
            language_item = wait.until(EC.element_to_be_clickable((By.XPATH, target_xpath)))
            driver.execute_script("arguments[0].click();", language_item)
            log_step(f"✅ 已点击语言：{language}")

            # 等待语言切换成功
            short_wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".language_val"), language))

        except Exception as e:
            err_msg = f"❌ {language} 点击失败:{str(e)}"
            log_step(err_msg)
            driver.save_screenshot(f"error_{language}.png")
            log_step(f"📸 已保存{language}错误截图")

    log_step("🎉 所有语言测试完成", step_start)
    driver.save_screenshot("language_test_result.png")
    log_step("📸 已保存整体结果截图 language_test_result.png")

except Exception as e:
    error_time = datetime.now().strftime("%H:%M:%S")
    print(f"❌ [{error_time}] 脚本全局执行失败:{e}")
    driver.save_screenshot("error_global.png")
finally:
    time.sleep(1)
    driver.quit()
    print("🔚 浏览器关闭")
    print(f"脚本总耗时:{time.time() - script_start_time:.2f}秒")
