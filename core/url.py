from core.server.wx_handler import WxHandler
from core.server.wxauthorize import WxSignatureHandler
import tornado.web
from core.server.page_handler import PageHandler
"""
web解析规则
"""

urlpatterns = [
    (r'/wx/signature', WxSignatureHandler),  # 微信签名
    (r'/wx/wxauthor', WxHandler),#网页授权处理
    (r'/wx/page/index',PageHandler)
   ]