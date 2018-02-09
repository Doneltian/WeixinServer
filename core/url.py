from core.server.wx_handler import WxHandler
from core.server.wxauthorize import WxSignatureHandler
import tornado.web
from core.server.page_handler import PageHandler
"""
web解析规则
"""

urlpatterns = [
    (r'/wxsignature', WxSignatureHandler),  # 微信签名
    (r'/page/(.*)', PageHandler),#加载第三方页面
    (r'/wx/wxauthor', WxHandler),#网页授权处理
   ]