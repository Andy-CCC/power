import os
import yaml


class DataUtil:
    """
    测试数据读取工具类
    """

    @staticmethod
    def load_yaml(file_name):
        """
    读取yaml文件

        :param file_name:
            yaml文件名称

        :return:
            dict类型数据
        """

        # 获取项目根目录
        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        # 拼接yaml文件路径
        file_path = os.path.join(
            base_dir,
            "data",
            file_name
        )

        # 判断文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"测试数据文件不存在: {file_path}"
            )

        # 读取yaml文件
        with open(
                file_path,
                "r",
                encoding="utf-8"
        ) as file:
            return yaml.safe_load(file)

    @staticmethod
    def get_case_data(file_name, case_name):
        """
        获取指定模块测试数据

        :param file_name:
            yaml文件

        :param case_name:
            yaml节点名称

        :return:
            测试数据
        """

        data = DataUtil.load_yaml(file_name)

        return data.get(case_name)
