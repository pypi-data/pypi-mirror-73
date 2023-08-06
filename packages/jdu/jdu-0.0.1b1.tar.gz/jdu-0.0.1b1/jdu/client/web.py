# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)
from jdu.core import exceptions
from jdu.api.web.m import M
from jdu.api.web.receive_code import ReceiveCode
from jdu.api.web.goods import Goods
from jdu.client.base import BaseClient, logger

class JDUWebBaseClient(BaseClient):
    def __init__(self, cookie, timeout=None, auto_retry=True, *args, **kwargs):
        super(JDUWebBaseClient, self).__init__(timeout, auto_retry, *args, **kwargs)
        self._cookie = cookie

    def _request(self, method, uri, **kwargs):
        return super(JDUWebBaseClient, self)._request(method, uri, **kwargs)

    def get_cookie(self):
        return self._cookie

class JDUWebUnionClient(JDUWebBaseClient):
    """
    针对 https://union.jd.com/api
    """

    goods = Goods()
    receive_code = ReceiveCode()

    def _top_result_processor(self, res, result, **kwargs):
        if 'code' in result and result['code'] != 200:
            code = result.get('code')
            message = result.get('message', '')
            logger.error("\n【请求地址】: %s\n【请求方法】: %s\n【请求参数】：%s \n%s\n【错误信息】：%s",
                         res.url, res.request.method, kwargs.get('params', ''), kwargs.get('data', ''), result)

            if code == 80001 or code == 402:
                raise exceptions.JDUClientAccessException(
                    code,
                    message,
                    client=self,
                    request=res.request,
                    response=res
                )
            else:
                raise exceptions.JDUClientException(
                    code,
                    message,
                    client=self,
                    request=res.request,
                    response=res
                )
        else:
            top_result = result.get('data')
        return top_result


class JDUWebApiClient(JDUWebBaseClient):
    """
    针对于 'https://api.m.jd.com/'
    """
    m = M()

    def _top_result_processor(self, res, result, **kwargs):
        if 'code' in result and result['code'] != 200:
            code = result.get('code')
            message = result.get('message', '')
            logger.error("\n【请求地址】: %s\n【请求方法】: %s\n【请求参数】：%s \n%s\n【错误信息】：%s",
                         res.url, res.request.method, kwargs.get('params', ''), kwargs.get('data', ''), result)

            if code == 80001 or code == 402:
                raise exceptions.JDUClientAccessException(
                    code,
                    message,
                    client=self,
                    request=res.request,
                    response=res
                )
            else:
                raise exceptions.JDUClientException(
                    code,
                    message,
                    client=self,
                    request=res.request,
                    response=res
                )
        else:
            top_result = result
        return top_result