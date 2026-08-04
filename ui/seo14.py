from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def log_step(msg):
    print(f"【{time.strftime('%H:%M:%S')}】{msg}")

# ---------------- 配置区 ----------------
BASE_URL = "https://www-h5.flextv9.com/"
# 搜索测试词列表，自行修改
search_words = [
    "我是刘邦",
    "今天是个好日子",
    "DemoTest"
]
# 等待时长
WAIT_SHORT = 3
# 统计变量
case_total = 0
case_pass = 0
case_fail = 0

# Chrome配置
chrome_options = Options()
chrome_options.binary_location = r"D:\chrome-test\chrome-win64\chrome.exe"
# 全屏启动
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, WAIT_SHORT)

try:
    log_step("打开网站")
    driver.get(BASE_URL)
    time.sleep(1.5)

    for keyword in search_words:
        case_total += 1
        log_step(f"========== 开始执行用例：搜索【{keyword}】 ==========")
        try:
            # 1.点击搜索按钮
            search_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".icon-search, [aria-label='Search']")))
            search_btn.click()
            time.sleep(0.5)

            # 2.点击输入框，休眠1s（你的要求）
            input_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='search']")))
            input_box.click()
            time.sleep(1)

            # 清空原有内容，输入关键词，回车搜索
            input_box.clear()
            input_box.send_keys(keyword)
            input_box.send_keys(Keys.ENTER)

            # 搜索结果加载等待
            time.sleep(2)
            log_step("⏸️ 停留2秒，查看搜索结果")

            # ====================== 【核心业务断言】 ======================
            no_data_display = False
            try:
                # 判断是否出现 No data
                wait.until(EC.visibility_of_element_located(
                    (By.XPATH, "//*[normalize-space(text())='No data']")
                ))
                no_data_display = True
            except Exception:
                no_data_display = False

            if no_data_display:
                log_step(f"ℹ️ 页面展示【No data】，关键词【{keyword}】无匹配剧集，预期场景")
            else:
                # 有结果场景校验
                result_header = wait.until(EC.visibility_of_element_located(
                    (By.XPATH, "//*[contains(text(),'results were found for')]")
                ))
                header_text = result_header.text
                assert keyword in header_text, f"顶部结果标题不含关键词，页面文本：{header_text}"
                assert "0 results" not in header_text, "页面异常：没有No data，但返回0 results"
                log_step(f"✅ 断言通过：【{keyword}】搜索结果正常渲染")
            # ===========================================================

            # 上下滑动3秒
            log_step("🔄 持续3秒上下滑动页面")
            start_time = time.time()
            while time.time() - start_time < 3:
                driver.execute_script("window.scrollBy(0,300)")
                time.sleep(0.4)
                driver.execute_script("window.scrollBy(0,-300)")
                time.sleep(0.4)

            # 返回首页
            home_logo = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img.logo, .flex-tv-logo")))
            home_logo.click()
            time.sleep(1)

            case_pass += 1
            log_step(f"✅【{keyword}】用例执行成功\n")

        except Exception as e:
            case_fail += 1
            log_step(f"❌【{keyword}】用例失败：{str(e)}")
            # 失败截图
            driver.save_screenshot(f"fail_{keyword}_{time.time()}.png")
            log_step("已保存失败截图")
            # 出错后回到首页，保证下一条用例环境干净
            try:
                driver.find_element(By.CSS_SELECTOR, "img.logo, .flex-tv-logo").click()
            except:
                driver.get(BASE_URL)
            time.sleep(1.5)

    # ============ 测试报告小结 ============
    log_step("\n==================== 测试执行小结 ====================")
    log_step(f"总执行用例数：{case_total}")
    log_step(f"成功用例：{case_pass}")
    log_step(f"失败用例：{case_fail}")
    success_rate = f"{(case_pass/case_total*100):.2f}%" if case_total>0 else "0%"
    log_step(f"成功率：{success_rate}")
    log_step("======================================================")

finally:
    log_step("执行完毕，关闭浏览器")
    driver.quit()
