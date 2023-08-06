'''
Flask-Jy-Share
~~~~~~~~~~~~~~~
Create social share component in Jinja2 template based on share.js.
:copyright: (c) 2020 by jiangyang.
:license: MIT, see LICENSE for more details.
'''
import re

from flask import (
    current_app,
    url_for,
    Markup,
    Blueprint,
    request,
)


class Share(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        '''
        初始化
        '''
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        # 注册扩展到 app.extensions 字典
        app.extensions['share'] = self
        
        # 把扩展类添加到模板上下文
        app.jinja_env.globals['share'] = self
        
        # 添加扩展配置
        app.config.setdefault('SHARE_SITES', 'weibo, wechat, douban, facebook, twitter, google, linkedin, qq, qzone')
        app.config.setdefault('SHARE_MOBILE_SITES', 'weibo, douban, qq, qzone')
        app.config.setdefault('SHARE_HIDE_ON_MOBILE', False)
        
        # 支持用户设置是否使用内置资源
        app.config.setdefault('SHARE_SERVE_LOCAL', False)
        # 创建蓝本
        blueprint = Blueprint('share', __name__, static_folder='static',
                static_url_path='/share' + app.static_url_path)
        app.register_blueprint(blueprint)

    @staticmethod
    def load(css_url=None, js_url=None):
        '''
        加载 share.js 资源

        :param css_url: 如果设置了, 就会使用这个 css_url
        :param js_url: 如果设置了, 就会使用这个 js_url
        :param serve_local: 如果设置为 True, 就使用本地资源
        '''
        if current_app.config['SHARE_SERVE_LOCAL']:
            css_url = url_for('share.static', filename='css/share.min.css')
            js_url = url_for('share.static', filename='js/share.min.js')
        if css_url is None:
            css_url = 'https://cdn.bootcss.com/social-share.js/1.0.16/css/share.min.css'
        if js_url is None:
            js_url = 'https://cdn.bootcss.com/social-share.js/1.0.16/js/social-share.min.js'
        return Markup('''<link rel="stylesheet" href="%s" type="text/css">\n
            <script src="%s"></script>''' % (css_url, js_url))

    @staticmethod
    def create(title='', sites=None, mobile_sites=None, align='left', addition_class=''):
        '''
        创建一个 share 组件.

        :param title: 标题.
        :param sites: 以 , 分隔的由站点组成的字符串, 支持的站点 name 有: weibo, wechat, douban, facebook, twitter, google, linkedin, qq, qzone.例如: `'weibo, wechat, qq'`.
        :param mobile_sites: 手机上显示的网站.
        :param align: 组件的对齐方式, 默认为 left.
        :param addition_class: the style class added to the share component.
        '''
        # 在移动设备上隐藏
        if current_app.config['SHARE_HIDE_ON_MOBILE']:
            platform = request.user_agent.platform
            if platform is not None:
                mobile_pattern = re.compile('android|fennec|iemobile|iphone|opera(?:mini|mobi)')
            
                m = re.match(mobile_pattern, platform)
                if m is not None:
                    return ''

        if sites is None:
            sites = current_app.config['SHARE_SITES']
        if mobile_sites is None:
            mobile_sites = current_app.config['SHARE_MOBILE_SITES']
        return Markup('''<div class="social-share %s" data-sites="%s" data-mobile-sites="%s" align="%s">%s</div>
            ''' % (addition_class, sites, mobile_sites, align, title))
