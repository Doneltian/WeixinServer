import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from core.server.wxmenu import WxMenuServer
from core.server.wxshedule import WxShedule
from core.url import urlpatterns

define('port', default=8000, help='run on the given port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "core/template"),
            static_path = os.path.join(os.path.dirname(__file__), "core/static"),
            debug = True,
            login_url = '/login',
            cookie_secret = 'MuG7xxacQdGPR7Svny1OfY6AymHPb0H/t02+I8rIHHE=',
        )
        super(Application,self).__init__(urlpatterns,**settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)

    # 执行定时任务
    wx_shedule = WxShedule()
    wx_shedule.excute()
    tornado.ioloop.IOLoop.current().start()



    wx_menu_server = WxMenuServer()
    # '''自定义菜单创建接口'''
    wx_menu_server.create_menu()
if __name__ == '__main__':
    main()