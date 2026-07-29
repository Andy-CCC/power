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
# chrome_options.add_argument("--disable-images") # 测试稳定后打开提速
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=chrome_options)
# 全局长等待仅用于页面初始化
wait = WebDriverWait(driver, 12)
# 业务操作统一使用短等待，大幅减少闲置时间
short_wait = WebDriverWait(driver, 3)
script_start_time = time.time()

# 搜索用例数据驱动列表
search_case_list = [
    {"case_id": "Search-001", "keyword": "我是刘邦", "desc": "常规中文正向搜索"},
    {"case_id": "Search-001", "keyword": "##############@@@@@@@@@@@@@@@@@@@@@@@", "desc": "常规中文正向搜索"},
    {"case_id": "Search-001", "keyword": "1", "desc": "常规中文正向搜索"},
    {"case_id": "Search-002", "keyword": "刘邦", "desc": "英文关键词搜索"},
    {"case_id": "Search-001", "keyword": "2", "desc": "常规中文正向搜索"},
    {"case_id": "Search-003", "keyword": "RUN", "desc": "数字英文混合搜索"}

]

def run_search_case(case_data):
    case_id = case_data["case_id"]
    keyword = case_data["keyword"]
    desc = case_data["desc"]
    case_start = log_step(f"===== 开始执行用例 {case_id}：{desc} =====")
    try:
        # 1.唤起搜索弹窗
        try:
            search_btn = short_wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-btn, [class*='search'] button, a[class*='search']")))
            search_btn.click()
        except:
            search_icon = short_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".icon-search")))
            search_icon.click()

        search_input = short_wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[type='search'], input[type='text'], input[placeholder*='搜索'], input[placeholder*='Search']")))
        search_input.click()
        search_input.clear()

        # 2.输入关键词+回车
        search_input.send_keys(keyword)
        log_step(f"已输入搜索内容：{keyword}", case_start)
        search_input.send_keys(Keys.RETURN)

        # 等待页面渲染完成
        try:
            short_wait.until(lambda d: d.execute_script("return document.readyState === 'complete'"))
        except Exception:
            log_step("搜索结果渲染超时，继续执行", case_start)

        # 需求1：停留2秒查看结果
        log_step("⏸️ 停留2秒，观察搜索结果")
        time.sleep(2)

        # 需求新增：上下滑动页面，持续3秒
        log_step("🔄 开始上下滚动页面，持续3秒")
        scroll_start = time.time()
        # 循环上下滚动，累计满3秒停止
        while time.time() - scroll_start < 3:
            # 向下滚动
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.4)
            # 向上滚动
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.4)

        # 截图保存当前结果页面
        driver.save_screenshot(f"{case_id}_result.png")

        # 3.点击logo返回首页
        logo = short_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.logo")))
        driver.execute_script("arguments[0].click();", logo)
        short_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".icon-search")))
        log_step(f"✅ {case_id} 执行完毕，已返回首页", case_start)

    except Exception as e:
        log_step(f"❌ {case_id} 执行失败：{str(e)}", case_start)
        driver.save_screenshot(f"{case_id}_error.png")
        # 异常兜底：强制返回首页，保证下一条正常执行
        try:
            logo = short_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.logo")))
            driver.execute_script("arguments[0].click();", logo)
            short_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".icon-search")))
            log_step(f"⚠️ {case_id} 异常，强制返回首页", case_start)
        except:
            log_step(f"⚠️ {case_id} 异常，无法点击logo")

try:
    # 初始打开网页
    step_start = log_step("🚀 正在打开 FlexTV 网页...")
    driver.get("https://www-h5.flextv9.com/")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".icon-search")))
    wait.until(lambda d: d.execute_script("return document.readyState === 'complete'"))
    log_step("✅ 页面加载完成", step_start)

    # 循环执行所有用例
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
