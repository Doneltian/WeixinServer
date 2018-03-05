
class WxMsgTemplate():
    """
    提供微信的消息模板
    """
    @staticmethod
    def reply_text(self, FromUserName, ToUserName, CreateTime, Content):
        """回复文本消息模板"""
        textTpl = """<xml> <ToUserName><![CDATA[%s]]></ToUserName> <FromUserName><![CDATA[%s]]></FromUserName> <CreateTime>%s</CreateTime> <MsgType><![CDATA[%s]]></MsgType> <Content><![CDATA[%s]]></Content></xml>"""
        out = textTpl % (FromUserName, ToUserName, CreateTime, 'text', Content)
        return out

    @staticmethod
    def reply_picandtext(self, FromUserName, ToUserName, CreateTime, ArticleCount,Title,Description ,PicUrl ,Url):
        """回复图文消息模板"""
        textTpl = """<xml><ToUserName>< ![CDATA[%s] ]></ToUserName><FromUserName>< ![CDATA[%s] ]></FromUserName><CreateTime>%s</CreateTime><MsgType>< ![CDATA[%s] ]></MsgType><ArticleCount>%s</ArticleCount><Articles><item><Title>< ![CDATA[%s] ]></Title> <Description>< ![CDATA[%s] ]></Description><PicUrl>< ![CDATA[%s] ]></PicUrl><Url>< ![CDATA[%s] ]></Url></item></Articles></xml>"""
        out = textTpl % (FromUserName, ToUserName, CreateTime, 'news', ArticleCount,Title,Description, PicUrl,Url)
        return out

    @staticmethod
    def reply_pic(self, FromUserName, ToUserName, CreateTime, MediaId):
        """回复图片消息模板"""
        textTpl = """<xml><ToUserName>< ![CDATA[toUser] ]></ToUserName><FromUserName>< ![CDATA[fromUser] ]></FromUserName><CreateTime>12345678</CreateTime><MsgType>< ![CDATA[image] ]></MsgType><Image><MediaId>< ![CDATA[media_id] ]></MediaId></Image></xml>"""
        out = textTpl % (FromUserName, ToUserName, CreateTime, 'image', MediaId)
        return out