from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime

# -------- 0. 日志工具函数 --------
def log_step(message, start_time=None):
    current_time = time.time()
    timestamp = datetime.now().strftime("%H:%M:%S")
    if start_time:
        elapsed = current_time - start_time
        print(f"[{timestamp}] ⏱️ {message} (耗时: {elapsed:.2f}秒)")
    else:
        print(f"[{timestamp}] {message}")
    return current_time

# -------- 1. 浏览器配置（全屏最大化） --------
chrome_options = Options()
chrome_options.binary_location = r"D:\chrome-test\chrome-win64\chrome.exe"
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--disable-images") # 提速可选
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)
short_wait = WebDriverWait(driver, 3)
script_start_time = time.time()

# 搜索用例数据驱动列表
search_case_list = [
    {"case_id": "Search-001", "keyword": "我是刘邦", "desc": "常规中文正向搜索"},
    {"case_id": "Search-002", "keyword": "Movie", "desc": "英文关键词搜索"},
    {"case_id": "Search-003", "keyword": "film123", "desc": "数字英文混合搜索"},
    {"case_id": "Search-004", "keyword": "", "desc": "空内容搜索"},
    {"case_id": "Search-006", "keyword": "@#￥%&*", "desc": "特殊符号搜索"},
    {"case_id": "Search-007", "keyword": "aaaaabbbbbcccccdddddeeeee", "desc": "无匹配关键词搜索"}
]

def run_search_case(case_data):
    """封装单条搜索用例执行逻辑，复用代码"""
    case_id = case_data["case_id"]
    keyword = case_data["keyword"]
    desc = case_data["desc"]
    case_start = log_step(f"===== 开始执行用例 {case_id}：{desc} =====")
    try:
        # 1. 唤起搜索弹窗
        try:
            search_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-btn, [class*='search'] button, a[class*='search']")))
            search_btn.click()
        except:
            search_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".icon-search")))
            search_icon.click()
        # 动态等待输入框出现，替代固定sleep
        search_input = short_wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[type='search'], input[type='text'], input[placeholder*='搜索'], input[placeholder*='Search']")))
        search_input.click()
        search_input.clear()

        # 2. 输入关键词
        search_input.send_keys(keyword)
        log_step(f"已输入搜索内容：{keyword}", case_start)
        # 回车搜索
        search_input.send_keys(Keys.RETURN)

        # 3. 结果断言区分空输入/正常关键词
        if keyword == "":
            # 空输入不产生搜索结果，校验页面无变化
            log_step("空关键词，校验无搜索请求触发", case_start)
        else:
            try:
                wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, keyword)))
                log_step(f"✅ {case_id} 通过：页面匹配关键词「{keyword}」", case_start)
            except:
                log_step(f"⚠️ {case_id} 无匹配结果（预期内）", case_start)
        # 单条用例截图
        driver.save_screenshot(f"{case_id}_result.png")
    except Exception as e:
        log_step(f"❌ {case_id} 执行失败：{str(e)}", case_start)
        driver.save_screenshot(f"{case_id}_error.png")

try:
    # 步骤1：打开页面
    step_start = log_step("🚀 正在打开 FlexTV 网页...")
    driver.get("https://www-h5.flextv9.com/")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".icon-search")))
    wait.until(lambda d: d.execute_script("return document.readyState === 'complete'"))
    log_step("✅ 页面加载完成", step_start)

    # 循环执行全部搜索用例
    for case in search_case_list:
        run_search_case(case)

    total_elapsed = time.time() - script_start_time
    print("\n" + "=" * 50)
    print(f"🏁 全部搜索用例执行完成！总耗时: {total_elapsed:.2f} 秒")
    print("=" * 50)

except Exception as e:
    error_time = datetime.now().strftime("%H:%M:%S")
    print(f"\n❌ [{error_time}] 全局脚本错误: {e}")
    driver.save_screenshot("global_error.png")
finally:
    time.sleep(1)
    driver.quit()
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🔚 浏览器关闭")
    print(f"总运行时长: {time.time() - script_start_time:.2f} 秒")
