from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# ===================== 配置区域 =====================
# Banner轮播图 完整CSS路径（你提供的DOM层级）
banner_locator = (By.CSS_SELECTOR, "#__nuxt > div.pc > div > div > div.home_content > div.hero-section > h3 > a")
# 左上角FlexTV Logo定位
logo_locator = (By.CSS_SELECTOR, "img.logo")
# 返回首页校验元素（搜索图标可见即代表回到首页）
home_check_locator = (By.CSS_SELECTOR, ".icon-search")
base_url = "https://www.flextv.cc/"
loop_total = 10       # 循环100次
stay_time = 5           # 播放页停留5秒
wait_long = WebDriverWait(None, 12)
wait_short = WebDriverWait(None, 3)
# ====================================================

# 浏览器初始化配置
chrome_options = Options()
chrome_options.binary_location = r"D:\chrome-test\chrome-win64\chrome.exe"
# chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=chrome_options)
# 给等待器绑定driver
wait_long._driver = driver
wait_short._driver = driver

# 统计变量
success_count = 0
fail_count = 0
fail_info_list = []

try:
    print(f"【初始化】访问网站：{base_url}")
    driver.get(base_url)
    # 等待首页加载完成
    wait_long.until(EC.visibility_of_element_located(home_check_locator))
    print(f"✅ 首页加载完成，即将开始{loop_total}次循环\n")

    for round_num in range(1, loop_total + 1):
        print(f"==================== 第 {round_num}/{loop_total} 轮 ====================")
        try:
            # 1. 定位Banner轮播链接，JS点击进入播放页
            print("步骤1：定位并点击Banner轮播图")
            banner_elem = wait_long.until(EC.element_to_be_clickable(banner_locator))
            driver.execute_script("arguments[0].click();", banner_elem)
            time.sleep(1)

            # 2. 播放页面停留5秒
            print(f"步骤2：进入播放器页面，停留{stay_time}秒")
            time.sleep(stay_time)

            # 3. 点击左上角FlexTV Logo返回首页
            print("步骤3：点击左上角FlexTV按钮回到首页")
            logo_elem = wait_long.until(EC.element_to_be_clickable(logo_locator))
            driver.execute_script("arguments[0].click();", logo_elem)
            time.sleep(1)

            # 4. 后置断言：校验成功回到首页
            wait_short.until(EC.visibility_of_element_located(home_check_locator))
            print(f"✅ 第{round_num}轮全部流程执行成功\n")
            success_count += 1

        except Exception as err:
            # 单轮失败处理：截图、记录错误、刷新页面恢复环境
            error_msg = f"第{round_num}轮执行失败：{str(err)}"
            print(f"❌ {error_msg}\n")
            driver.save_screenshot(f"loop_{round_num}_error.png")
            fail_info_list.append(error_msg)
            fail_count += 1
            # 兜底刷新首页，避免下一轮环境污染
            driver.get(base_url)
            time.sleep(2)

    # ===================== 循环结束 输出汇总报告 =====================
    print("=" * 70)
    print("                    循环执行测试报告")
    print("=" * 70)
    print(f"计划循环总次数：{loop_total}")
    print(f"成功完成轮次：{success_count}")
    print(f"失败轮次数量：{fail_count}")
    if loop_total > 0:
        rate = (success_count / loop_total) * 100
        print(f"执行成功率：{rate:.2f} %")
    if fail_count > 0:
        print("\n❌ 失败明细清单：")
        for msg in fail_info_list:
            print(f"  - {msg}")
    else:
        print("\n🎉 全部100轮循环执行无任何失败！")
    print("=" * 70)

except Exception as global_err:
    print(f"\n❌ 脚本全局异常终止：{str(global_err)}")
    driver.save_screenshot("global_crash_error.png")
finally:
    print("\n执行完毕，关闭浏览器进程")
    time.sleep(2)
    driver.quit()