#!/usr/bin/env python
# -*- encoding: utf8 -*-
import os
import re
import sys
import json
import time
import binascii
import textwrap
from collections import defaultdict

from multiprocessing.dummy import Pool as ThreadPool

try:
    import cPickle as pickle
except ImportError:
    import pickle

import requests
from dateutil.parser import parse as date_parse

from cms.util import MyLogger, User


reload(sys)
sys.setdefaultencoding('utf-8')


class LIMS(object):
    base_url = 'http://lims.novogene.com/STARLIMS11.novogene'

    def __init__(self, logger=None):
        self.logger = logger or MyLogger()
        self.session = requests.session()

    def login(self, username, password):
        # step1: get user info
        url = self.base_url + '/Authentication.GetUserInfoHtml.lims'

        username = username.upper()

        password = [binascii.b2a_hex(each.encode()).decode()
                    for each in password]
        password = ''.join(list(map('{:0>4}'.format, password))).upper()

        payload = [username, password]
        user_info = self.session.post(url, json=payload).json()

        if not user_info:
            self.logger.error(
                'login failed, please check your username and password!')
            return False

        self.logger.info('login successful!')
        dept = user_info[0]['Tables'][0]['Rows'][0]['Dept']
        role = user_info[1]['Tables'][0]['Rows'][0]['ROLE']

        url = self.base_url + '/Authentication.LoginMobile.lims'
        payload = {
            'user': username,
            'password': password,
            'dept': dept,
            'role': role,
            'platforma': 'HTML',
        }
        result = self.session.get(url, params=payload).text

        return True

    def get_data(self, subprojectid):

        self.logger.debug('>>> crawling subprojectid: {}'.format(subprojectid))

        stage_dict = {}

        url = self.base_url + '/Runtime_Support.GetDataAsJson.lims'
        payload = [
            'ReportManagement.kf_Operation_Process',
            [subprojectid, '', '', '']
        ]
        
        res = None
        for n in range(5):
            try:
                res = self.session.post(url, json=payload, timeout=300).json()
                break
            except Exception as e:
                self.logger.warn('[{}] failed get data for {} as: {}'.format(n, subprojectid, e.message))
                time.sleep(5)

        if res is None:
            self.logger.error('failed get data for subprojectid: {}'.format(subprojectid))
            return {subprojectid: stage_dict}

        if not res['Tables']:
            return {subprojectid: stage_dict}

        rows = res['Tables'][0]['Rows']

        # ==========================
        # 运营开始时间：最早的下单时间
        # 信息开始时间：最晚的路径时间
        # ==========================

        for row in rows:
            # print json.dumps(row, indent=2, ensure_ascii=False)
            stage_code = row[unicode('分期')]

            path_date = row[unicode('路径时间')]
            path_datetime = date_parse(path_date) if path_date else None

            xiadan_date = row[unicode('下单时间')]
            xiadan_datetime = date_parse(xiadan_date) if xiadan_date else None

            if stage_code not in stage_dict:
                stage_dict[stage_code] = defaultdict(dict)

            if path_datetime:
                if ('path_date' not in stage_dict[stage_code]) or (path_datetime > stage_dict[stage_code]['path_date']):
                    stage_dict[stage_code]['path_date'] = path_datetime

            if xiadan_datetime:
                if ('xiadan_date' not in stage_dict[stage_code]) or (xiadan_datetime < stage_dict[stage_code]['xiadan_date']):
                    stage_dict[stage_code]['xiadan_date'] = xiadan_datetime

        return {subprojectid: stage_dict}


def main(**args):

    start_time = time.time()

    logger = MyLogger('LIMS', format='[%(asctime)s %(funcName)s %(levelname)s %(threadName)s] %(message)s', **args)

    user = User(section='lims', **args)
    username, password = user.get_user_pass()

    lims = LIMS(logger=logger)

    if lims.login(username, password):
        user.save(username, password)
    else:
        exit(1)

    if os.path.isfile(args['subprojectid']):
        subprojectids = open(args['subprojectid']).read().strip().split('\n')
    else:
        subprojectids = args['subprojectid'].split(',')

    subprojectids = set(subprojectids)

    if args['prefix']:
        subprojectids = filter(lambda x: x.startswith(args['prefix']), subprojectids)

    subproject_num = len(subprojectids)

    logger.info('Total subprojectid: {}'.format(subproject_num))

    stage_data = {}

    if args['threads'] > 1:
        logger.info('start crawling with threads: {threads}'.format(**args))

        pool = ThreadPool(args['threads'])

        try:
            result = pool.map_async(lims.get_data, subprojectids)
            pool.close()
            pool.join()
        except KeyboardInterrupt:
            pool.terminate()
            pool.join()

        for each in result.get():
            subprojectid, stage_dict = each.items()[0]
            if stage_dict:
                stage_data.update(stage_dict)
    else:
        for n, subprojectid in enumerate(subprojectids, 1):
            logger.debug('[{n}/{subproject_num}] completed'.format(**locals()))
            data = lims.get_data(subprojectid)
            stage_data.update(data)

    with open(args['out'], 'wb') as out:
        pickle.dump(stage_data, out)

    logger.info('save file: {out}'.format(**args))
    logger.info('time used: {:.1f}s'.format(time.time() - start_time))


def parser_add_lims(parser):

    parser.description = __doc__
    parser.epilog = textwrap.dedent('''
        \033[36mexamples:
            %(prog)s ...
        \033[0m
    ''')

    parser.add_argument('-u', '--username', help='the username to login lims')
    parser.add_argument('-p', '--password', help='the password to login lims')

    parser.add_argument('-id', '--subprojectid',
                        help='the subprojectid to query, string or file contains id', required=True)

    parser.add_argument(
        '-prefix', '--prefix', help='only use stagecode which starts with prefix')

    parser.add_argument(
        '-o', '--out', help='the output filename [default: %(default)s]', default='lims.stage.pkl')

    parser.add_argument(
        '-t', '--threads', help='the threads used to crawl [default: %(default)s]', type=int, default=8)

    parser.set_defaults(func=main)
