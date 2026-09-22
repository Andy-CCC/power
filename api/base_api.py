import time
import requests
import allure


from common.config import BASE_URL
from common.headers import get_headers



class BaseApi:
    """
    接口请求基类


    所有业务接口继承：

    UserApi
    VideoApi
    PayApi


    统一处理：

    1. URL拼接
    2. headers
    3. GET请求
    4. POST请求
    5. 请求日志
    6. 响应时间
    7. Allure附件
    8. 代理处理

    """



    def __init__(self):

        """
        初始化session
        """

        self.session = requests.Session()


        # =====================================
        # 关闭系统代理
        #
        # 解决：
        #
        # requests.exceptions.ProxyError
        #
        # 开代理软件导致接口失败
        #
        # =====================================

        self.session.trust_env = False



    # =====================================
    # GET请求
    # =====================================

    def get(
            self,
            path,
            params=None,
            name=None
    ):
        """
        GET请求


        示例：

        self.get(
            path="/webMoreRecommended",
            params={
                "page_no":1,
                "page_size":28
            }
        )

        """


        return self.request(

            method="GET",

            path=path,

            params=params,

            name=name

        )



    # =====================================
    # POST请求
    # =====================================

    def post(
            self,
            path,
            json=None,
            name=None
    ):
        """
        POST请求


        示例：

        self.post(

            path="/login",

            json=data

        )

        """


        return self.request(

            method="POST",

            path=path,

            json=json,

            name=name

        )



    # =====================================
    # 核心请求方法
    # =====================================

    def request(
            self,
            method,
            path,
            params=None,
            json=None,
            name=None
    ):
        """
        所有请求统一入口
        """



        # ===============================
        # 拼接URL
        # ===============================

        url = BASE_URL + path



        # ===============================
        # 获取headers
        # ===============================

        headers = get_headers()



        # ===============================
        # 请求日志
        # ===============================

        print("\n" + "=" * 60)

        print(
            "接口名称:",
            name
        )

        print(
            "请求方式:",
            method
        )

        print(
            "请求URL:",
            url
        )

        print(
            "请求参数:",
            params if params else json
        )

        print("=" * 60)



        # ===============================
        # 开始计时
        # ===============================

        start_time = time.time()



        try:


            response = self.session.request(

                method=method,

                url=url,

                headers=headers,

                params=params,

                json=json,

                timeout=30

            )


        except requests.exceptions.ProxyError as e:


            print(
                "代理异常，请检查代理设置:",
                e
            )


            raise e



        except requests.exceptions.RequestException as e:


            print(
                "请求异常:",
                e
            )


            raise e



        # ===============================
        # 结束计时
        # ===============================

        end_time = time.time()



        response_time = round(

            (end_time - start_time)
            * 1000,

            2

        )



        # ===============================
        # 响应日志
        # ===============================

        print(
            "响应状态码:",
            response.status_code
        )


        print(
            "响应时间:",
            response_time,
            "ms"
        )


        print(
            "响应内容:",
            response.text
        )



        # ===============================
        # Allure报告附件
        # ===============================


        allure.attach(

            url,

            name="请求URL",

            attachment_type=allure.attachment_type.TEXT

        )



        allure.attach(

            method,

            name="请求方式",

            attachment_type=allure.attachment_type.TEXT

        )



        allure.attach(

            str(params if params else json),

            name="请求参数",

            attachment_type=allure.attachment_type.TEXT

        )



        allure.attach(

            response.text,

            name="响应内容",

            attachment_type=allure.attachment_type.TEXT

        )



        allure.attach(

            str(response_time) + " ms",

            name="响应时间",

            attachment_type=allure.attachment_type.TEXT

        )



        return response