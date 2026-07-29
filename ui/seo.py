from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# -------- 1. 浏览器配置 --------
chrome_options = Options()
chrome_options.binary_location = r"D:\chrome-test\chrome-win64\chrome.exe"  # 替换成你的实际路径
# chrome_options.add_argument("--headless")  # 如需后台运行，取消注释
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)  # 全局等待

try:
    # -------- 2. 打开目标网页 --------
    print("🚀 正在打开 FlexTV 网页...")
    driver.get("https://www-h5.flextv9.com/")

    # 等待页面关键元素出现（首页的 "Watch Free" 链接或按钮）
    wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Watch Free")))
    print("✅ 页面加载成功！")

    # -------- 3. 执行一次搜索操作（示例）--------
    # 3.1 点击搜索图标（顶部的 "Search" 链接）
    search_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Search")))
    search_link.click()
    print("🔍 已点击搜索入口")
    time.sleep(1)  # 等待搜索框展开或跳转

    # 3.2 在搜索框中输入关键词（根据实际页面，可能需要调整选择器）
    # 提示：搜索框可能是 input 标签，也可能是一个弹窗，需按F12确认
    # 这里提供两种常见写法：
    try:
        # 写法1：如果搜索框在当前页面可见
        search_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search'], input[placeholder*='搜索']")))
        search_input.clear()
        search_input.send_keys("我是刘邦")
        search_input.send_keys(Keys.RETURN)
        print("📝 已搜索: 我是刘邦")
    except:
        # 写法2：如果点击Search后跳转到搜索页面
        print("⚠️ 未在当前页找到搜索输入框，可能已跳转，尝试在跳转后的页面定位...")
        search_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'], input[placeholder*='Search']")))
        search_input.send_keys("我是刘邦" + Keys.RETURN)
        print("📝 已在新页面搜索: 我是刘邦")

    # -------- 4. 从结果中点击第一个剧集（示例）--------
    # 等待搜索结果加载，然后点击包含 "我是刘邦" 的剧集卡片或链接
    # 提示：结果列表可能是 <a> 标签或 <div> 卡片，需观察实际HTML
    first_result = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "我是刘邦")))
    first_result.click()
    print("🎬 已点击第一个搜索结果")

    # -------- 5. 尝试点击播放按钮 --------
    # 进入剧集详情页后，寻找 "Watch Free" 或 "Play" 按钮
    # 注意：可能会先弹出VIP购买弹窗
    try:
        play_button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                             "//button[contains(text(),'Watch Free')] | //button[contains(text(),'Play')] | //*[contains(@class,'play-btn')]")))
        play_button.click()
        print("▶️ 已点击播放按钮")
    except:
        print("⚠️ 未找到播放按钮，可能页面需要VIP或存在弹窗，尝试关闭弹窗...")
        # 尝试关闭可能出现的VIP弹窗（示例：点击关闭按钮或点击背景）
        try:
            close_btn = driver.find_element(By.CSS_SELECTOR, ".modal-close, .close-btn, [aria-label='Close']")
            close_btn.click()
            print("❌ 已关闭弹窗")
            time.sleep(1)
            # 再次尝试点击播放
            play_button = driver.find_element(By.XPATH, "//button[contains(text(),'Watch Free')]")
            play_button.click()
            print("▶️ 已点击播放按钮（弹窗关闭后）")
        except:
            print("⛔ 未能处理弹窗或播放按钮，请手动检查页面结构")

    # 等待几秒，观察视频是否播放（或页面状态）
    time.sleep(5)

    # 可选：保存截图用于调试
    driver.save_screenshot("flextv_automation_result.png")
    print("📸 最终状态截图已保存")

except Exception as e:
    print(f"❌ 自动化过程中出现错误: {e}")
    driver.save_screenshot("error_screenshot.png")
    print("📸 错误截图已保存为 error_screenshot.png")

finally:
    # 关闭浏览器
    driver.quit()
    print("🔚 浏览器已关闭")