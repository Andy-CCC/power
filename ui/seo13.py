from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime

def log_step(message, start_time=None):
    current_time = time.time()
    timestamp = datetime.now().strftime("%H:%M:%S")
    if start_time:
        elapsed = current_time - start_time
        print(f"[{timestamp}] ⏱️ {message} (耗时: {elapsed:.2f}秒)")
    else:
        print(f"[{timestamp}] {message}")
    return current_time

# 浏览器配置
chrome_options = Options()
chrome_options.binary_location = r"D:\chrome-test\chrome-win64\chrome.exe"
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 12)
short_wait = WebDriverWait(driver, 3)
script_start_time = time.time()

# ===================== 测试统计变量（报告使用） =====================
total_case = 0
pass_case = 0
fail_case = 0
fail_list = []

# ===================== 分层用例集，按需切换 =====================
# 冒烟用例（3条，快速回归）
smoke_case_list = [
    {"case_id": "S01", "keyword": "我是刘邦", "desc": "中文正向搜索"},
    {"case_id": "S02", "keyword": "Movie", "desc": "英文搜索"},
    {"case_id": "S03", "keyword": "aaaa1111bbbb2222", "desc": "无匹配关键词"}
]

# 全量回归用例（8条，版本上线完整测试）
full_case_list = [
    {"case_id": "F01", "keyword": "我是刘邦", "desc": "中文正向搜索"},
    {"case_id": "F02", "keyword": "Movie", "desc": "英文搜索"},
    {"case_id": "F03", "keyword": "film2025", "desc": "字母数字混合"},
    {"case_id": "F04", "keyword": "", "desc": "空输入回车搜索"},
    {"case_id": "F05", "keyword": "@#￥%&*!~", "desc": "特殊符号搜索"},
    {"case_id": "F06", "keyword": "aaaaaabbbbbcccccdddddeeeee", "desc": "超长文本无匹配"},
    {"case_id": "F07", "keyword": "123456789", "desc": "纯数字搜索"},
    {"case_id": "F08", "keyword": "我是刘邦Movie123！", "desc": "中英数字符号混合"}
]

# 切换执行集：smoke_case_list / full_case_list
run_case_list = full_case_list

def run_search_case(case_data):
    global total_case, pass_case, fail_case
    case_id = case_data["case_id"]
    keyword = case_data["keyword"]
    desc = case_data["desc"]
    case_start = log_step(f"===== 开始执行用例 {case_id}：{desc} =====")
    try:
        # 1. 点击搜索按钮，增加重试机制
        click_success = False
        retry = 0
        while retry < 2 and not click_success:
            try:
                search_btn = short_wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-btn, [class*='search'] button, a[class*='search']")))
                search_btn.click()
                click_success = True
            except Exception:
                retry += 1
                log_step(f"⚠️ 搜索按钮点击失败，重试第{retry}次")
                time.sleep(0.3)
        if not click_success:
            search_icon = short_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".icon-search")))
            search_icon.click()

        # 定位输入框
        search_input = short_wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[type='search'], input[type='text'], input[placeholder*='搜索'], input[placeholder*='Search']")))
        search_input.click()
        time.sleep(1) # 点击输入框休眠1秒
        search_input.clear()
        search_input.send_keys(keyword)
        log_step(f"已输入搜索内容：{keyword}", case_start)
        search_input.send_keys(Keys.RETURN)

        # 等待页面渲染完成
        try:
            short_wait.until(lambda d: d.execute_script("return document.readyState === 'complete'"))
        except Exception:
            log_step("搜索结果渲染超时，继续执行", case_start)

        # 需求1：停留2秒查看结果
        log_step("⏸️ 停留2秒，人工观测搜索结果")
        time.sleep(2)

        # 需求2：上下滚动页面3秒
        log_step("🔄 持续3秒上下滚动浏览页面")
        scroll_start = time.time()
        while time.time() - scroll_start < 3:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.4)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.4)

        # 截图
        driver.save_screenshot(f"{case_id}_result.png")

        # 返回首页
        logo = short_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.logo")))
        driver.execute_script("arguments[0].click();", logo)
        short_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".icon-search")))
        log_step(f"✅ {case_id} 执行完毕，已重置回首页", case_start)

        # 统计成功用例
        total_case += 1
        pass_case += 1

    except Exception as e:
        log_step(f"❌ {case_id} 执行失败：{str(e)}", case_start)
        driver.save_screenshot(f"{case_id}_error.png")
        # 统计失败用例
        total_case += 1
        fail_case += 1
        fail_list.append(f"{case_id}｜{desc}｜报错信息:{str(e)}")
        # 异常兜底切回首页
        try:
            logo = short_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.logo")))
            driver.execute_script("arguments[0].click();", logo)
            short_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".icon-search")))
        except:
            pass

try:
    step_start = log_step("🚀 打开FlexTV网页")
    driver.get("https://www-h5.flextv9.com/")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".icon-search")))
    wait.until(lambda d: d.execute_script("return document.readyState === 'complete'"))
    # 全局初始化缓冲，解决第一次搜索过快组件未挂载
    time.sleep(1)
    log_step("✅ 页面全部资源与交互组件初始化完成", step_start)

    # 循环执行选中的用例集
    for case in run_case_list:
        run_search_case(case)

    total_elapsed = time.time() - script_start_time
    # ===================== 测试报告小结 =====================
    print("\n" + "=" * 70)
    print("                📋 搜索模块自动化测试报告小结")
    print("=" * 70)
    print(f"✅ 执行总用例数量：{total_case}")
    print(f"🟢 通过用例：{pass_case}")
    print(f"🔴 失败用例：{fail_case}")
    if total_case > 0:
        success_rate = (pass_case / total_case) * 100
        print(f"📊 执行成功率：{success_rate:.2f} %")
    print(f"⏱️ 脚本总耗时：{total_elapsed:.2f} 秒")
    if fail_list:
        print("\n❌ 失败用例清单：")
        for item in fail_list:
            print(f"    {item}")
    else:
        print("\n🎉 所有用例全部执行通过，无失败案例！")
    print("=" * 70)

except Exception as e:
    err_time = datetime.now().strftime("%H:%M:%S")
    print(f"\n❌ [{err_time}] 全局脚本异常：{e}")
    driver.save_screenshot("global_error.png")
finally:
    time.sleep(1)
    driver.quit()
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🔚 浏览器关闭")
