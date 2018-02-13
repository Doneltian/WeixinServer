import tornado.web

from core.logger_helper import logger


class PageHandler(tornado.web.RequestHandler):
    """
    微信handler处理类
    """
    def post(self, flag):
        logger.debug('微信handler处理类】<<<<<<<<<' + flag)
        if flag == 'index':
            """首页"""
            self.render('index')

    def get(self):
        logger.debug('微信handler处理类】》》》》》》》》》》')
        self.render('index.html')