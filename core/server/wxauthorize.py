from core.logger_helper import logger
import hashlib
import tornado.web


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
