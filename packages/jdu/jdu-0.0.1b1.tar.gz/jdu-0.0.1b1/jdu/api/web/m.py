# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)
import json
import uuid

import arrow

from jdu.core import exceptions
from jdu.api.base import JDUWebAPI


class M(JDUWebAPI):

    def get_content_type(self):
        return None

    def list_order_sku(self, order_ids=None, start_time=None, end_time=None, order_status=0, opt_type=1, page_no=1,
                       page_size=20, login_type=3):

        url = 'https://api.m.jd.com/'

        ext_headers = {
            'authority': 'api.m.jd.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'referer': 'https://union.jd.com/order',
            'origin': 'https://union.jd.com',
            'sec-fetch-site': 'same-site',
        }

        if not order_ids:
            order_ids = []

        if not isinstance(order_ids, (list)):
            order_ids = [order_ids]

        now = arrow.utcnow().to('+08:00')

        if not end_time:
            end_time = now.replace(hour=23, minute=59, second=59).format('YYYY-MM-DD HH:mm:ss')

        if not start_time:
            start_time = now.shift(days=-7).replace(hour=0, minute=0, second=0).format('YYYY-MM-DD HH:mm:ss')

        body_params = {
            'startTime': start_time,
            'endTime': end_time,
            'orderStatus': order_status,
            'optType': opt_type,
        }

        if order_ids:
            body_params['orderIds'] = order_ids

        body = {
            'funName': 'listOrderSku',
            'param': body_params,
            'page': {
                'pageNo': page_no,
                'pageSize': page_size,
            }
        }
        params = {
            'appid': 'u',
            'body': json.dumps(body),
            'functionId': 'listOrderSku',
            'loginType': login_type,
        }

        return self.get(url, params=params, ext_headers=ext_headers)
