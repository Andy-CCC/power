# api/user_api.py

from api.base_api import BaseApi


class UserApi(BaseApi):
    """
    用户模块接口
    """

    def get_user_info(self):
        """
        获取个人信息
        """
        return self.get(path="/webUserInfo",name='【获取个人信息】')
    def get_banner(self):
        '''
        读取首页banner
        '''
        return self.get(path="/web/index/banner",name='【读取首页banner】')