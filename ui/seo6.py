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
# 可选：关闭自动化提示条
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)
short_wait = WebDriverWait(driver, 5)
# 记录开始时间
script_start_time = time.time()

try:
    # ============================================
    # 1. 打开网站
    # ============================================
    step_start = log_step("🚀 正在打开 FlexTV...")
    driver.get("https://www-h5.flextv9.com/")
    # 等待语言按钮出现
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".language_val")))
    # 额外等待页面完全渲染，避免loading阻塞hover事件
    time.sleep(1)
    log_step("✅ 页面加载成功", step_start)

    # ============================================
    # 2. 测试语言切换
    # ============================================
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
            # 重新定位语言入口
            language_btn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".language_val")))

            # 方式1：模拟鼠标悬浮，增加停留时间触发下拉动画
            ActionChains(driver).move_to_element(language_btn).pause(0.8).perform()
            log_step("🖱️ 鼠标悬浮语言按钮，等待下拉菜单展开")

            # 兜底：如果悬浮不生效，JS强制触发mouseover事件
            driver.execute_script("""
                const target = arguments[0];
                const mouseOverEvt = new MouseEvent('mouseover', {bubbles: true, cancelable: true});
                target.dispatchEvent(mouseOverEvt);
            """, language_btn)
            time.sleep(0.5)

            # 等待下拉容器ul可见
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".language_ul")))
            # 等待所有语言li渲染完成
            items = short_wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".language_ul li")))
            print(f"[{language}] 当前语言下拉数量：", len(items))
            for item in items:
                print(f"- {item.text}")

            # 兼容空格/嵌套标签的XPath匹配规则
            target_xpath = f"//ul[@class='language_ul']/li[normalize-space(.)='{language}']"
            language_item = wait.until(EC.element_to_be_clickable((By.XPATH, target_xpath)))

            # JS点击防止遮挡
            driver.execute_script("arguments[0].click();", language_item)
            log_step(f"✅ 已点击语言：{language}")

            # 动态等待页面语言切换完成，替代固定sleep
            short_wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".language_val"), language))

        except Exception as e:
            err_msg = f"❌ {language} 点击失败:{str(e)}"
            log_step(err_msg)
            # 单个语言失败单独截图，方便排查悬浮无菜单问题
            driver.save_screenshot(f"error_{language}.png")
            log_step(f"📸 已保存{language}错误截图")

    log_step("🎉 所有语言测试完成", step_start)
    # 整体测试完成截图
    driver.save_screenshot("language_test_result.png")
    log_step("📸 已保存整体结果截图 language_test_result.png")

except Exception as e:
    error_time = datetime.now().strftime("%H:%M:%S")
    print(f"❌ [{error_time}] 脚本全局执行失败:{e}")
    driver.save_screenshot("error_global.png")
    print("📸 已保存全局错误截图")
finally:
    time.sleep(2)
    driver.quit()
    print("🔚 浏览器关闭")
    print(f"脚本总耗时:{time.time() - script_start_time:.2f}秒")
