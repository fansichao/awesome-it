#!/usr/bin/env python
# -*- coding: utf-8 -*-
u""" Python HTTP 请求一览
"""

import logging

import requests

def http_request(url, msg="", method="GET", is_logging=False, **kwargs):
    u""" 执行需要的 HTTP 请求命令

    功能:
        整合了所有 HTTP 参数请求

    :param str url: 链接
    :param str msg: 信息
    :param str method: 请求方式

    get - params=data 
    post - data=data headers=headers
    """

    # TODO GET params 不支持循环嵌套的数据. 例如{'properties': {'data_mark': '20191119064014'}}

    try:
        method_lis = ['GET', 'POST', 'HEAD', 'OPTIONS', 'PUT', 'DELETE', 'TRACE', 'CONNECT']
        method = method if method.upper() in method_lis else method_lis[0]
        r = getattr(requests, method.lower(), None)(url, **kwargs)
        try:
            logging.info('>> %s \n[%s][URL]: %s' % (msg, method, urlparse.unquote(r.url)))
            ret = r.json()
        except Exception as e:
            if is_logging:
                logging.error(traceback.print_exc())
                logging.error(r.status_code)
                logging.error(r.reason)
            ret = ""
        return ret
    except Exception as e:
        logging.error(traceback.print_exc())
        logging.error(e)
        return ""

