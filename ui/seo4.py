from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime


# -------- 0. 计时工具函数 --------
def log_step(message, start_time=None):
    """打印带时间戳的步骤日志，并返回当前时间"""
    current_time = time.time()
    timestamp = datetime.now().strftime("%H:%M:%S")
    if start_time:
        elapsed = current_time - start_time
        print(f"[{timestamp}] ⏱️ {message} (耗时: {elapsed:.2f}秒)")
    else:
        print(f"[{timestamp}] {message}")
    return current_time

# -------- 1. 浏览器配置 --------
chrome_options = Options()
chrome_options.binary_location = r"D:\chrome-test\chrome-win64\chrome.exe"  # 替换成你的实际路径
#加上这行代码后，Chrome 浏览器会在后台运行，不会显示任何浏览器窗口
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

# 记录整个脚本的开始时间
script_start_time = time.time()

try:
    # ============================================
    # 步骤1：打开页面
    # ============================================
    step_start = log_step("🚀 正在打开 FlexTV 网页...")
    driver.get("https://www-h5.flextv9.com/")

    # 等待页面加载完成（等待搜索图标出现）
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".icon-search")))
    log_step("✅ 页面加载成功！", step_start)

    # ============================================
    # 步骤2：点击搜索按钮
    # ============================================
    step_start = log_step("🔍 正在定位并点击搜索按钮...")
    try:
        # 尝试点击包含搜索图标的父级元素
        search_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-btn, [class*='search'] button, a[class*='search']")))
        search_btn.click()
        log_step("✅ 已点击搜索按钮（父级元素）", step_start)
    except:
        # 备选方案：直接点击图标本身
        search_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".icon-search")))
        search_icon.click()
        log_step("✅ 已点击搜索按钮（图标元素）", step_start)

    # 等待搜索框动画/弹窗出现
    time.sleep(0.5)

    # ============================================
    # 步骤3：点击输入框
    # ============================================
    step_start = log_step("🖱️ 正在定位并点击搜索输入框...")
    try:
        search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                              "input[type='search'], input[type='text'], input[placeholder*='搜索'], input[placeholder*='Search']")))
        search_input.click()
        log_step("✅ 已点击搜索输入框", step_start)
    except Exception as e:
        log_step(f"⚠️ 点击输入框失败: {e}，尝试备选定位...", step_start)
        search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input")))
        search_input.click()
        log_step("✅ 已点击搜索输入框（备选定位）", step_start)

    # 清空输入框
    search_input.clear()

    # ============================================
    # 步骤4：输入内容
    # ============================================
    step_start = log_step("📝 正在输入搜索关键词...")
    search_keyword = "我是刘邦"
    search_input.send_keys(search_keyword)
    log_step(f"✅ 已输入内容: '{search_keyword}'", step_start)

    time.sleep(0.5)

    # ============================================
    # 步骤5：按回车搜索
    # ============================================
    step_start = log_step("⏎ 正在按回车键执行搜索...")
    search_input.send_keys(Keys.RETURN)
    log_step("✅ 已按回车键，搜索已触发", step_start)

    # ============================================
    # 步骤6：等待搜索结果（带超时保护）
    # ============================================
    step_start = log_step("⏳ 等待搜索结果加载...")
    try:
        # 等待页面出现变化（搜索词出现或某个结果元素出现）
        wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, search_keyword)))
        log_step(f"🎉 搜索成功！页面已包含关键词: '{search_keyword}'", step_start)
    except Exception as e:
        log_step(f"⚠️ 搜索结果验证超时: {e}", step_start)
        # 即使验证失败，也保存当前状态供分析

    # 保存截图
    driver.save_screenshot("search_result.png")
    log_step("📸 搜索结果截图已保存为 search_result.png")

    # ============================================
    # 执行完成，汇总
    # ============================================
    total_elapsed = time.time() - script_start_time
    print("\n" + "=" * 50)
    print(f"🏁 整个场景执行完成！总耗时: {total_elapsed:.2f} 秒")
    print("=" * 50)

except Exception as e:
    # ============================================
    # 错误处理
    # ============================================
    error_time = datetime.now().strftime("%H:%M:%S")
    print(f"\n❌ [{error_time}] 自动化过程中出现严重错误: {e}")
    driver.save_screenshot("error_screenshot.png")
    print(f"📸 错误截图已保存为 error_screenshot.png")
    # 打印当前页面标题，辅助定位
    try:
        print(f"📄 当前页面标题: {driver.title}")
    except:
        pass

finally:
    # ============================================
    # 关闭浏览器
    # ============================================
    time.sleep(2)
    driver.quit()
    end_time = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{end_time}] 🔚 浏览器已关闭")
    print(f"📊 脚本总运行时间: {time.time() - script_start_time:.2f} 秒")
