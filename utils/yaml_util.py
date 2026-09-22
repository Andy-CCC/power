import yaml


class YamlUtil:
    """
    yaml文件读取工具
    """

    @staticmethod
    def read_yaml(path):
        """
        读取yaml文件
        """

        with open(
                path,
                "r",
                encoding="utf-8"
        ) as f:
            data = yaml.safe_load(f)

        return data
