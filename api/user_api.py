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
    def get_user_spending_list(self,page_no=1,page_size=10):
        '''
        获取用户消费记录
        :return:
        '''
        params={
            "page_no":page_no,
            "page_size":page_size
        }
        #传参
        return self.get(path="/webUserSpendingList",params=params,name="【获取用户消费记录】")
    def get_user_webUserTopUpList(self,page_no=1,page_size=10):
        #获取用户充值记录
        # https://api-t.flextv.cc/webUserTopUpList?page_no=1&page_size=10
        params = {
            "page_no": page_no,
            "page_size": page_size
        }
        return self.get(path='/webUserTopUpList',params=params,name='【获取用户充值记录】')
    #https://api-t.flextv.cc/webGetSeriesDetailContent?series_id=XVZdDmxZwp
    def get_video_webGetSeriesDetailContent(self,series_id):
        #获取短剧详细数据
        params = {
            "series_id": series_id
        }
        return self.get(path='/webGetSeriesDetailContent',params=params,name='【获取短剧详细数据】')
