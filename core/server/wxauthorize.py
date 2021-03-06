import json
import urllib
import requests
import threading
from core.logger_helper import logger
import hashlib
import tornado.web
import xml.etree.ElementTree as ET
import time
import core.server.wxconfig
import core.server.wxmenu
import core.server.singleton

class WxSignatureHandler(tornado.web.RequestHandler):
    """
    微信服务器签名验证, 消息回复
    check_signature: 校验signature是否正确
    """
    def data_received(self,chunk):
        pass

    def get(self):
        try:
            signature = self.get_argument('signature')
            timestamp = self.get_argument('timestamp')
            nonce = self.get_argument('nonce')
            echostr = self.get_argument('echostr')

            logger.debug(
                '微信sign校验,signature=' + signature + ',&timestamp=' + timestamp + '&nonce=' + nonce + '&echostr=' + echostr)

            result = self.check_signature(signature, timestamp, nonce)
            if result:
                logger.debug('微信sign校验,返回echostr=' + echostr)
                self.write(echostr)
            else:
                logger.error('微信sign校验,---校验失败')
        except Exception as e:
            logger.error('微信sign校验,---Exception' + str(e))

    def check_signature(self, signature, timestamp, nonce):
        """校验token是否正确"""
        token = 'donel666666'
        L = [timestamp, nonce, token]
        L.sort()
        s = L[0] + L[1] + L[2]
        sha1 = hashlib.sha1(s.encode('utf-8')).hexdigest()
        logger.debug('sha1=' + sha1 + '&signature=' + signature)
        return sha1 == signature

    def post(self, *args, **kwargs):
        body = self.request.body
        logger.debug('微信消息回复中心】收到用户消息'+ str(body.decode('utf-8')))
        data = ET.fromstring(body)
        ToUserName = data.find('ToUserName').text
        FromUserName = data.find('FromUserName').text
        MsgType = data.find('MsgType').text

        if MsgType == 'text' or MsgType == 'voice':
            '''文本消息 or 语音消息'''
            try:
                MsgId = data.find("MsgId").text
                if MsgType == 'text':
                    Content = data.find('Content').text  # 文本消息内容
                elif MsgType == 'voice':
                    Content = data.find('Recognition').text  # 语音识别结果，UTF8编码
                if Content == u'你好':
                    reply_content = '您好,请问有什么可以帮助您的吗?'
                else:
                    # 查找不到关键字,默认回复
                    reply_content = "客服小儿智商不够用啦~"
                if reply_content:
                    CreateTime = int(time.time())
                    out = self.reply_text(FromUserName, ToUserName, CreateTime, reply_content)
                    self.write(out)
            except Exception as e:
                    logger.error(e)
        elif MsgType == 'event':
            '''接受事件推送'''
            try:
                Event = data.find('Event').text
                if Event == 'subscribe':
                    # 关注事件
                    wxinit =  WxInit()
                    wxinit.menu_init();


                    #发送欢迎语
                    CreateTime = int(time.time())
                    reply_content = '欢迎关注我的公众号~'
                    out = self.reply_text(FromUserName, ToUserName, CreateTime, reply_content)
                    self.write(out)
                elif Event == 'VIEW':
                    #跳转
                    logger.debug('微信菜单跳转跳转跳转！！！！！！！！！！！！！！！！】')
            except Exception as e:
                logger.error(e)





class WxAuthorServer(core.server.singleton.Singleton):
    """
    微信网页授权server
    get_code_url                            获取code的url
    get_auth_access_token                   通过code换取网页授权access_token
    refresh_token                           刷新access_token
    check_auth                              检验授权凭证（access_token）是否有效
    get_userinfo                            拉取用户信息
    """

    """授权后重定向的回调链接地址，请使用urlencode对链接进行处理"""
    REDIRECT_URI = 'http://120.78.174.191/wx/wxauthor'

    """
        应用授权作用域
        snsapi_base （不弹出授权页面，直接跳转，只能获取用户openid）
        snsapi_userinfo （弹出授权页面，可通过openid拿到昵称、性别、所在地。并且，即使在未关注的情况下，只要用户授权，也能获取其信息）
        """
    SCOPE = 'snsapi_base'
    # SCOPE = 'snsapi_userinfo'

    """通过code换取网页授权access_token"""
    get_access_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?'

    """拉取用户信息"""
    get_userinfo_url = 'https://api.weixin.qq.com/sns/userinfo?'

    @classmethod
    def get_code_url(cls, state):
        """获取code 的url"""
        dict = {'redirect_uri': cls.REDIRECT_URI}
        logger.debug('【微信网页授权】获取网页授权的redirect_uri>>>>>【' + cls.REDIRECT_URI + '】')
        redirect_url = urllib.parse.urlencode(dict)
        # redirect_url = urllib.parse.urlencode(cls.REDIRECT_URI)
        logger.debug('【微信网页授权】获取网页授权的redirect_uri的encode>>>>>【' + redirect_url + '】')
        author_get_code_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&%s&response_type=code&scope=%s&state=%s#wechat_redirect' % (
            core.server.wxconfig.WxConfig.AppID, redirect_url, cls.SCOPE, state)
        logger.debug('【微信网页授权】获取网页授权的code的url>>>>' + author_get_code_url)
        return author_get_code_url

    def get_auth_access_token(self, code):
        """通过code换取网页授权access_token"""
        url = self.get_access_token_url + 'appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (
            core.server.wxconfig.WxConfig.AppID, core.server.wxconfig.WxConfig.AppSecret, code)
        r = requests.get(url)
        logger.debug('【微信网页授权】通过code换取网页授权access_token的Response[' + str(r.status_code) + ']')
        if r.status_code == 200:
            res = r.text
            logger.debug('【微信网页授权】通过code换取网页授权access_token>>>>' + res)
            json_res = json.loads(res)
            if 'access_token' in json_res.keys():
                return json_res
            elif 'errcode' in json_res.keys():
                errcode = json_res['errcode']


class WxInit(core.server.singleton.Singleton):
    """
    微信关注后初始化
    create_menu_data：创建主页面菜单

    """
    wx_menu_server = core.server.wxmenu.WxMenuServer()

    def create_menu_data(self,url):
        """创建菜单数据"""
        menu_data = {'button' : []} #大彩蛋
        menu_Index0 = {
            'type':'view',
            'name': '测试菜单1',
            'url': url
        }
        menu_data['button'].append((menu_Index0))
        MENU_DATA = json.dumps(menu_data , ensure_ascii= False)
        logger.debug('【微信自定义菜单】创建菜单数据MENU_DATA[' + str(MENU_DATA) + ']')
        return MENU_DATA

    def menu_init(self):
        """初始化菜单"""
        # 创建自定义菜单

        #获取该按钮对应网页授权的url
        url = WxAuthorServer.get_code_url('menuIndex0')
        logger.debug('微信创建自定义菜单】url = ' + url)

        data = self.create_menu_data(url)

        # '''自定义菜单创建接口'''
        WxInit.wx_menu_server.create_menu(data)