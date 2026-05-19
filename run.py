import pytest
import os
import platform
import shutil
from config.env_config import BASE_DIR

def generate_allure_report():
    """生成Allure报告（兼容多系统）"""
    results_dir = os.path.join(BASE_DIR, "reports", "allure-results")
    report_dir = os.path.join(BASE_DIR, "reports", "allure-report")

    # 清空旧报告
    if os.path.exists(report_dir):
        shutil.rmtree(report_dir)

    # 生成报告
    system = platform.system()
    try:
        if system == "Windows":
            os.system(f"allure generate {results_dir} -o {report_dir} --clean")
        else:
            os.system(f"bash -c 'allure generate {results_dir} -o {report_dir} --clean'")
        print(f"\n✅ Allure报告已生成：{os.path.join(report_dir, 'index.html')}")
    except Exception as e:
        print(f"\n⚠️ 生成Allure报告失败（需安装Allure）：{e}")

if __name__ == "__main__":
    # 执行用例
    pytest.main()
    # 生成报告
    generate_allure_report()
    # 自动打开报告（Windows）
    try:
        report_index = os.path.join(BASE_DIR, "reports", "allure-report", "index.html")
        os.startfile(report_index)
    except:
        pass