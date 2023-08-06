# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
from .chromeU import ChromeU
from scrapy.http import HtmlResponse


class ScrapyMiddlewareU(PyApiB):
    """
    scrapyMiddleware相关封装工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    @classmethod
    def process_request(cls, request, spider):
        if spider.crawlType == 'chrome':
            chromeU = ChromeU().setConfig(isHide=True)
            webdri = chromeU.loadUrl(request.url)
            spider.chromeDo(chromeU, request._meta)
            html = chromeU.toHTML()
            chromeU.quit()
            return HtmlResponse(url=request.url,
                                body=html,
                                request=request,
                                encoding='utf-8')
