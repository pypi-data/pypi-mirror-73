# -*- coding: utf-8 -*-
# Authored by: Josh (joshzda@gmail.com)
import json

from jdu.api.base import JDUOpenAPI


class Order(JDUOpenAPI):

    def query(self, query_type, query_time, page_no=1, page_size=20, child_union_id=None, key=None):
        """
        订单查询接口
        文档: https://union.jd.com/openplatform/api/10419
        :param page_no: 页码，返回第几页结果
        :param page_size: 每页包含条数，上限为500
        :param query_type: 订单时间查询类型(1：下单时间，2：完成时间，3：更新时间)
        :param query_time: 查询时间，建议使用分钟级查询，格式：yyyyMMddHH、yyyyMMddHHmm或yyyyMMddHHmmss，如201811031212 的查询范围从12:12:00--12:12:59
        :param child_union_id: 子站长ID（需要联系运营开通PID账户权限才能拿到数据），childUnionId和key不能同时传入
        :param key: 其他推客的授权key，查询工具商订单需要填写此项，childUnionid和key不能同时传入
        :return:
        """


        api_method = 'jd.union.open.order.query'

        order_req = {
            'pageNo': page_no,
            'pageSize': page_size,
            'type': query_type,
            'time': query_time,
            'childUnionId': child_union_id,
            'key': key,
        }

        params = {
            'orderReq': order_req
        }

        def process_result(result, response, client=None, **kwargs):
            if result.get('jd_union_open_order_query_response'):
                result = result.get('jd_union_open_order_query_response')
                _result = result.get('result')
                if _result:
                    result = json.loads(_result)
            return result

        return self.get(api_method, params, result_processor=process_result)

    def row_query(self, query_type, start_time, end_time, page_index=1, page_size=20, child_union_id=None, key=None, fields=None):
        """
        订单行查询接口
        文档: https://union.jd.com/openplatform/api/12707
        :param query_type: 订单时间查询类型(1：下单时间，2：完成时间，3：更新时间)
        :param start_time: 开始时间 格式yyyy-MM-dd HH:mm:ss，与endTime间隔不超过1小时
        :param end_time: 结束时间 格式yyyy-MM-dd HH:mm:ss，与startTime间隔不超过1小时
        :param page_index: 页码
        :param page_size: 每页包含条数，上限为500
        :param child_union_id: 子站长ID（需要联系运营开通PID账户权限才能拿到数据），childUnionId和key不能同时传入
        :param key: 其他推客的授权key，查询工具商订单需要填写此项，childUnionid和key不能同时传入
        :param fields: 出参数据筛选，多项逗号分隔
        :return:
        """
        api_method = 'jd.union.open.order.row.query'

        order_req = {
            'pageIndex': page_index,
            'pageSize': page_size,
            'type': query_type,
            'startTime': start_time,
            'endTime': end_time,
            'childUnionId': child_union_id,
            'key': key,
            'fields': fields,
        }

        params = {
            'orderReq': order_req
        }

        def process_result(result, response, client=None, **kwargs):
            if result.get('jd_union_open_order_row_query_response'):
                result = result.get('jd_union_open_order_row_query_response')
                _result = result.get('result')
                if _result:
                    result = json.loads(_result)
            return result

        return self.get(api_method, params, result_processor=process_result)