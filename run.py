import os
import json
import shutil
import subprocess
import time

import pytest

from common.config import ALLURE_PATH


if __name__ == "__main__":

    start_time = time.time()


    # ===============================
    # 项目根目录
    # ===============================

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )


    # ===============================
    # Allure路径配置
    # ===============================

    result_path = os.path.join(
        BASE_DIR,
        "reports",
        "allure-results"
    )


    report_path = os.path.join(
        BASE_DIR,
        "reports",
        "allure-report"
    )


    print("==============================")
    print("Allure结果目录:")
    print(result_path)

    print("Allure报告目录:")
    print(report_path)

    print("==============================")


    # ===============================
    # 清理历史报告
    # ===============================

    if os.path.exists(result_path):

        shutil.rmtree(result_path)


    if os.path.exists(report_path):

        shutil.rmtree(report_path)


    os.makedirs(result_path)



    # =================================================
    # 1. 生成Allure Environment环境信息
    # =================================================

    environment_file = os.path.join(
        result_path,
        "environment.properties"
    )

    environment_content = """
    Environment=Test Environment
    Project=Official Website API Automation
    ApiUrl=https://api-t.flextv.cc
    FrontendUrl=https://www-h5.flextv9.com
    Framework=Python + Pytest
    Report=Allure
    RequestType=HTTP
    TokenMode=Fixed Token
    TestMode=Guest
    """


    with open(
        environment_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            environment_content.strip()
        )


    print("Allure Environment生成完成")



    # =================================================
    # 2. 生成Allure Categories分类
    # =================================================

    categories_file = os.path.join(
        result_path,
        "categories.json"
    )


    categories_content = [

        {
            "name": "接口断言失败",
            "matchedStatuses": [
                "failed"
            ],
            "messageRegex": ".*AssertionError.*"
        },

        {
            "name": "接口请求异常",
            "matchedStatuses": [
                "broken"
            ],
            "messageRegex": ".*(ConnectionError|Timeout|ProxyError|RequestException).*"
        },

        {
            "name": "自动化代码异常",
            "matchedStatuses": [
                "broken"
            ],
            "messageRegex": ".*(KeyError|TypeError|AttributeError|IndexError).*"
        }

    ]


    with open(
        categories_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            categories_content,
            f,
            ensure_ascii=False,
            indent=4
        )


    print("Allure Categories生成完成")



    # =================================================
    # 3. 生成Allure Executor执行信息
    # =================================================


    executor_file = os.path.join(
        result_path,
        "executor.json"
    )


    executor_content = {

        "name": "接口自动化测试",

        "type": "pytest",

        "buildName": "测试环境接口自动化",

        "buildOrder": 1,

        "reportName": "Allure测试报告",

        "executor": "Eden"

    }


    with open(
        executor_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            executor_content,
            f,
            ensure_ascii=False,
            indent=4
        )


    print("Allure Executor生成完成")



    # ===============================
    # 执行pytest
    # ===============================

    print("==============================")
    print("开始执行接口自动化测试")
    print("==============================")


    pytest.main(
        [
            "-vs",
            "--alluredir",
            result_path
        ]
    )



    # ===============================
    # 生成Allure报告
    # ===============================

    print("==============================")
    print("开始生成Allure报告")
    print("==============================")


    generate_cmd = (

        f'"{ALLURE_PATH}" generate '

        f'"{result_path}" '

        f'-o "{report_path}" '

        f'--clean'

    )


    result = subprocess.run(
        generate_cmd,
        shell=True
    )



    if result.returncode == 0:


        print("==============================")
        print("Allure报告生成成功")
        print("==============================")


        # ===============================
        # 打开Allure报告
        # ===============================

        open_cmd = (

            f'"{ALLURE_PATH}" open '

            f'"{report_path}"'

        )


        subprocess.Popen(
            open_cmd,
            shell=True
        )


    else:

        print("==============================")
        print("Allure报告生成失败")
        print("==============================")



    end_time = time.time()


    print(
        f"总执行时间：{end_time-start_time:.2f} 秒"
    )