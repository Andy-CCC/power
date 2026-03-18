import pytest
import os
import platform
from config.env_config import BASE_DIR


def generate_allure_report():
    """生成Allure报告（兼容Windows/macOS/Linux）"""
    # 原始数据目录
    results_dir = os.path.join(BASE_DIR, "reports", "allure-results")
    # 报告输出目录
    report_dir = os.path.join(BASE_DIR, "reports", "allure-report")

    # 1. 先清空旧报告（避免缓存）
    if os.path.exists(report_dir):
        import shutil
        shutil.rmtree(report_dir)

    # 2. 生成报告（兼容不同系统的命令）
    system = platform.system()
    try:
        if system == "Windows":
            # Windows用cmd执行
            os.system(f"allure generate {results_dir} -o {report_dir} --clean")
        else:
            # macOS/Linux用bash执行
            os.system(f"bash -c 'allure generate {results_dir} -o {report_dir} --clean'")
        print(f"Allure报告已生成：{os.path.join(report_dir, 'index.html')}")
    except Exception as e:
        print(f"生成Allure报告失败：{e}")
        return False

    # 3. 自动打开报告（兼容多系统）
    try:
        index_html = os.path.join(report_dir, "index.html")
        if system == "Windows":
            os.startfile(index_html)  # Windows打开文件
        elif system == "Darwin":  # macOS
            os.system(f"open {index_html}")
        else:  # Linux
            os.system(f"xdg-open {index_html}")
    except Exception as e:
        print(f"自动打开报告失败，请手动打开：{index_html}")

    return True


if __name__ == "__main__":
    # 第一步：执行pytest用例，生成allure-results
    pytest.main(["-v", "--alluredir=./reports/allure-results"])

    # 第二步：生成并打开Allure报告
    generate_allure_report()