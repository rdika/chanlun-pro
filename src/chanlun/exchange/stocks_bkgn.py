import json
import os
import random
import time
from typing import Tuple

import akshare as ak
from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams
from tqdm.auto import tqdm

"""
股票板块概念
"""


class StocksBKGN(object):

    def __init__(self):
        self.file_name = os.path.split(os.path.realpath(__file__))[0] + '/stocks_bkgn.json'

        self.cache_file_bk = None

    def reload_ths_bkgn(self):
        """
        下载更新保存新的板块概念信息
        通过 同花顺 接口获取板块概念

        """
        error_msgs = []
        stock_industrys = {}
        ak_industry = ak.stock_board_industry_name_ths()
        for _, b in tqdm(ak_industry.iterrows()):
            b_name = b['name']
            b_code = b['code']
            try_nums = 0
            while True:
                try:
                    time.sleep(random.randint(4, 5))
                    # 获取板块的成分股
                    b_stocks = ak.stock_board_cons_ths(b_code)
                    for _, s in b_stocks.iterrows():
                        s_code = s['代码']
                        if s_code not in stock_industrys.keys():
                            stock_industrys[s_code] = []
                        stock_industrys[s_code].append(b_name)
                except Exception as e:
                    time.sleep(60)
                    try_nums += 1
                    if try_nums >= 10:
                        msg = f'{b_name} {b_code} 行业板块获取成分股异常：{e}'
                        error_msgs.append(msg)
                        print(msg)
                        break
                finally:
                    break

        stock_concepts = {}
        ak_concept = ak.stock_board_concept_name_ths()
        for _, b in tqdm(ak_concept.iterrows()):
            b_name = b['概念名称']
            b_code = b['代码']
            try_nums = 0
            while True:
                try:
                    time.sleep(random.randint(4, 5))
                    # 获取概念的成分股
                    b_stocks = ak.stock_board_cons_ths(b_code)
                    for _, s in b_stocks.iterrows():
                        s_code = s['代码']
                        if s_code not in stock_concepts.keys():
                            stock_concepts[s_code] = []
                        stock_concepts[s_code].append(b_name)
                except Exception as e:
                    time.sleep(60)
                    try_nums += 1
                    if try_nums >= 10:
                        msg = f'{b_name} {b_code} 概念板块获取成分股异常：{e}'
                        error_msgs.append(msg)
                        print(msg)
                        break
                finally:
                    break

        with open(self.file_name, 'w', encoding='utf-8') as fp:
            json.dump({'hy': stock_industrys, 'gn': stock_concepts}, fp)

        print('错误信息：', error_msgs)
        return True

    def reload_dfcf_bkgn(self):
        """
        下载更新保存新的板块概念信息
        通过 东方财富 接口获取板块概念

        """
        error_msgs = []
        stock_industrys = {}
        ak_industry = ak.stock_board_industry_name_em()
        for _, b in tqdm(ak_industry.iterrows()):
            b_name = b['板块名称']
            b_code = b['板块代码']
            try_nums = 0
            while True:
                try:
                    time.sleep(random.randint(1, 3))
                    # 获取板块的成分股
                    b_stocks = ak.stock_board_industry_cons_em(b_name)
                    for _, s in b_stocks.iterrows():
                        s_code = s['代码']
                        if s_code not in stock_industrys.keys():
                            stock_industrys[s_code] = []
                        stock_industrys[s_code].append(b_name)
                except Exception as e:
                    time.sleep(60)
                    try_nums += 1
                    if try_nums >= 10:
                        msg = f'{b_name} {b_code} 行业板块获取成分股异常：{e}'
                        error_msgs.append(msg)
                        print(msg)
                        break
                finally:
                    break

        stock_concepts = {}
        ak_concept = ak.stock_board_concept_name_em()
        for _, b in tqdm(ak_concept.iterrows()):
            b_name = b['板块名称']
            b_code = b['板块代码']
            try_nums = 0
            while True:
                try:
                    time.sleep(random.randint(1, 3))
                    # 获取概念的成分股
                    b_stocks = ak.stock_board_concept_cons_em(b_name)
                    for _, s in b_stocks.iterrows():
                        s_code = s['代码']
                        if s_code not in stock_concepts.keys():
                            stock_concepts[s_code] = []
                        stock_concepts[s_code].append(b_name)
                except Exception as e:
                    time.sleep(60)
                    try_nums += 1
                    if try_nums >= 10:
                        msg = f'{b_name} {b_code} 概念板块获取成分股异常：{e}'
                        error_msgs.append(msg)
                        print(msg)
                        break
                finally:
                    break

        with open(self.file_name, 'w', encoding='utf-8') as fp:
            json.dump({'hy': stock_industrys, 'gn': stock_concepts}, fp)

        print('错误信息：', error_msgs)
        return True

    def reload_tdx_bkgn(self):
        """
        下载更新保存新的板块概念信息
        通过 通达信 接口获取板块概念

        """
        stock_industrys = {}  # 保存行业的股票信息
        stock_concepts = {}  # 保存概念的股票信息

        # tdx_host = best_ip.select_best_ip('stock')
        tdx_host = {'ip': '221.194.181.176', 'port': 7709}
        api = TdxHq_API(raise_exception=True, auto_retry=True)
        with api.connect(tdx_host['ip'], tdx_host['port']):
            # 获取行业
            hy_infos = api.get_and_parse_block_info(TDXParams.BLOCK_DEFAULT)
            for _hy in hy_infos:
                _code = _hy['code']
                if _code not in stock_industrys.keys():
                    stock_industrys[_code] = []
                stock_industrys[_code].append(_hy['blockname'])
                stock_industrys[_code] = list(set(stock_industrys[_code]))

            # 获取概念
            gn_infos = api.get_and_parse_block_info(TDXParams.BLOCK_GN)
            for _gn in gn_infos:
                _code = _gn['code']
                if _code not in stock_concepts.keys():
                    stock_concepts[_code] = []
                stock_concepts[_code].append(_gn['blockname'])
                stock_concepts[_code] = list(set(stock_concepts[_code]))

        with open(self.file_name, 'w', encoding='utf-8') as fp:
            json.dump({'hy': stock_industrys, 'gn': stock_concepts}, fp)

        return True

    def __file_bkgns(self) -> Tuple[dict, dict]:
        if self.cache_file_bk is None:
            with open(self.file_name, 'r', encoding='utf-8') as fp:
                bkgns = json.load(fp)
            self.cache_file_bk = bkgns
        return self.cache_file_bk['hy'], self.cache_file_bk['gn']

    def get_code_bkgn(self, code: str):
        """
        获取代码板块概念
        """
        hys, gns = self.__file_bkgns()
        code_hys = []
        code_gns = []
        if code in hys.keys():
            code_hys = hys[code]
        if code in gns.keys():
            code_gns = gns[code]
        return {'HY': code_hys, 'GN': code_gns}

    def get_codes_by_hy(self, hy_name):
        """
        根据行业名称，获取其中的股票代码列表
        """
        hys, gns = self.__file_bkgns()
        codes = []
        for _code, _hys in hys.items():
            if hy_name in _hys:
                codes.append(_code)

        return codes

    def get_codes_by_gn(self, gn_name):
        """
        根据概念名称，获取其中的股票代码列表
        """
        hys, gns = self.__file_bkgns()
        codes = []
        for _code, _gns in gns.items():
            if gn_name in _gns:
                codes.append(_code)

        return codes


if __name__ == '__main__':
    """
    更新行业概念信息并保存
    """
    bkgn = StocksBKGN()
    # 重新更新并保存行业与板块信息
    # bkgn.reload_ths_bkgn()

    # 获取代码的板块概念信息
    code_bkgn = bkgn.get_code_bkgn('301080')
    print(code_bkgn)

    # 根据行业获取其中的代码
    # codes = bkgn.get_codes_by_hy('珠宝首饰')
    # print(codes)

    # 根据概念获取其中的代码
    # codes = bkgn.get_codes_by_gn('电子竞技')
    # print(codes)
