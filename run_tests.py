#!/usr/bin/env python3
"""
API自动化测试框架运行入口
"""
import sys
import os
import pytest
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='API自动化测试框架')

    parser.add_argument(
        '--env',
        choices=['dev', 'test', 'prod'],
        default='test',
        help='测试环境 (默认: test)'
    )

    parser.add_argument(
        '--tests',
        nargs='+',
        help='指定要运行的测试文件或目录'
    )

    parser.add_argument(
        '--mark',
        help='只运行指定标记的测试用例'
    )

    parser.add_argument(
        '--report',
        choices=['html', 'xml', 'allure'],
        default='html',
        help='测试报告类型 (默认: html)'
    )

    parser.add_argument(
        '--parallel',
        type=int,
        default=0,
        help='并行执行测试的进程数 (0表示不并行)'
    )

    parser.add_argument(
        '--reruns',
        type=int,
        default=0,
        help='失败重试次数'
    )

    return parser.parse_args()


def run_tests():
    """运行测试"""
    args = parse_args()

    # 设置环境变量
    os.environ['API_TEST_ENV'] = args.env

    # pytest参数
    pytest_args = [
        '-v',  # 详细输出
        '--tb=short',  # 简洁的错误回溯
        f'--html=reports/report_{args.env}.html',
        '--self-contained-html',
        '--capture=sys',  # 捕获输出
    ]

    # 添加测试路径
    if args.tests:
        pytest_args.extend(args.tests)
    else:
        pytest_args.append('test_cases')

    # 标记过滤
    if args.mark:
        pytest_args.append(f'-m {args.mark}')

    # 并行执行
    if args.parallel > 0:
        pytest_args.extend(['-n', str(args.parallel)])

    # 失败重试
    if args.reruns > 0:
        pytest_args.extend(['--reruns', str(args.reruns)])

    # Allure报告
    if args.report == 'allure':
        allure_dir = project_root / 'reports' / 'allure-results'
        allure_dir.mkdir(parents=True, exist_ok=True)
        pytest_args.extend([
            '--alluredir', str(allure_dir)
        ])

    print(f"运行测试，环境: {args.env}")
    print(f"pytest参数: {pytest_args}")

    # 运行测试
    exit_code = pytest.main(pytest_args)

    # 生成Allure报告
    if args.report == 'allure' and exit_code == 0:
        import subprocess
        report_dir = project_root / 'reports' / 'allure-report'
        subprocess.run([
            'allure', 'generate', str(allure_dir),
            '-o', str(report_dir),
            '--clean'
        ])
        print(f"Allure报告已生成: {report_dir}")

    sys.exit(exit_code)


if __name__ == '__main__':
    run_tests()