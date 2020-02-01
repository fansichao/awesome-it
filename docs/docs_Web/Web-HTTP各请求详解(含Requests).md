# Web-HTTP 各请求详解

tags: HTTP GET POST Requests 2019 年 11 月 TODO

## HTTP 请求 含义&区别

- [HTTP 中 GET 与 POST 的区别](https://www.jianshu.com/p/7b9b44e850c8)
- [浅谈 HTTP 中 GET、POST 用法以及它们的区别](https://www.cnblogs.com/williamjie/p/9099940.html)
  [HTTP Request GET, HEAD, POST, PUT, DELETE, OPTIONS, TRACE Methods](https://www.cnblogs.com/Herzog3/p/5881411.html)

[python 用 GET,POST,PUT,DELETE 方式向 HTTP 提交数据](https://blog.csdn.net/zhangqi_gsts/article/details/52823704)

[浅谈 HTTP 中 Get 与 Post 的区别-表格对比](https://blog.csdn.net/heise668/article/details/51725228)
[GET 和 POST 究竟有什么区别](https://blog.csdn.net/LeeSirbupt/article/details/80778474)

### Header 详解

## Requests 模块使用

### 完整样例封装代码

```python

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
```
