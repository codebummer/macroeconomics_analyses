from urllib.request import urlopen, Request
import sqlite3
import pandas as pd
import os, io, json, zipfile, glob
from datetime import datetime

from . import dart_list
from . import dart_report
from . import dart_finstate
from . import dart_share
from . import dart_event
from . import dart_regstate
from . import dart_utils

api_key = API_KEY
url = 

class OpenDartReader():
    
    #Initiate corp_code for a company's ID code
    def __init__(self, api_key):

        #Create a cache directory if it does not exist
        docs_cache_dir = 'docs_cache'
        if not os.path.exist(docs_cache_dir):
            os.makedirs(docs_cache_dir)
        
        #Read and return a document if it exists
        fn = 'opendartreader_corp_codes_{}.pkl'.format(datetime.tody().strftime('%Y%m%d'))
        fn_cache = os.path.join(docs_cache_dir)
        for fn_rm in glob.glob(os.path.join(docs_cache_dir, 'opendartreader_corp_codes_*')):
            if fn_rm == fn_cache:
                continue
            os.remove(fn_rm)
        if not os.path.exists(fn_cache):
            df = dart_list.corp_codes(api_key)
            df.to_pickle(fn_cache)

        self.corp_codes = pd.read_pickle(fn_cache)
        self.api_key = api_key

    #1. Public Information
    #1-1. Search information needed
    def list(self, corp=None, start=None, end=None, kind='', kind_detail='', final=True):
    
        '''
        DART 보고서의 목록을 DataFrame으로 반환
        * corp: 종목코드 (고유번호, 법인명도 가능)
        * start: 조회 시작일 (기본값: 1990-01-01')
        * end: 조회 종료일 (기본값: 당일)
        * kind: 보고서 종류:  A=정기공시, B=주요사항보고, C=발행공시, D=지분공시, E=기타공시, 
                            F=외부감사관련, G=펀드공시, H=자산유동화, I=거래소공시, J=공정위공시
        * final: 최종보고서 여부 (기본값: True)
        '''

        if corp:
            corp_code = self.find_corp_code(corp)
            if not corp_code:
                raise ValueError(f'could not find "{corp}"')
        else:
            corp_code = ''
        return dart_list.list(self.api_key, corp_code, start, end, kind, kind_detail, final)

    #1-2. A Company's Financial Statements
    def company(self, corp):
        corp_code = self.find_corp_code(corp)
        return dart_list.company(self.api_key, corp_code)

    def company_by_name(self, name):
        df = self.corp_codes[self.corp_codes['corp_name'].str.contains(name)]
        corp_code_list = list(df['corp_code'])
        return dart_list.company_by_name(self.api_key, corp_code_list)

    #1-3. Public Documents Original
    def document(self, rcp_no, cache=True):
        return dart_list.document(self.api_key, rcp_no, cache=cache)
    
    #1-4. Corporation Codes - corp to copr_code
    def fin_corp_code(self, corp):
        if not corp.isdigit():
            df = self.corp_codes[self.corp_codes['corp_name'] == corp]
        elif corp.isdigit() and len(corp) == 6:
            df = self.corp_codes[self.corp_codes['stock_code'] == corp]
        else:
            df = self.corp_codes[self.corp_codes['corp_code'] == corp]
        return None if df.empty else df.iloc[0]['corp_code']
    
    #2. Business Reports
    def report(self, corp, key_word, bsns_year, reprt_code='11011'):
        corp_code = self.find_corp_code(corp)
        if not corp_code:
            raise ValueError(f'could not find "{corp}"')
        return dart_report.report(self.api_key, corp_code, key_word, bsns_year, reprt_code)
    
    #3. Financial Statements of Listed Companies
    #3-1. Financial Statements of a Single Company
    #3-2. Financial Statements of Multiple Companies
    def finstate(self, corp, bsns_year, reprt_code='11011'):
        if ',' in corp:
            code_list = [self.find_corp_code(c.strip()) for c in corp.split(',')]
            corp_code = ','.join(code_list)
        else:
            corp_code = self.find_corp_code(corp)
        return dart_finstate.finstate(self.api_key, corp_code, bsns_year, reprt_code)
    
    #3-3. Original Financial Statements (XBRL)
    def finstate_xml(self, rcp_no, save_as):
        return dart_finstate.finstate_xml(self.api_key, rcp_no, save_as=save_as)
    
    #3-4. All Financial Statements of A Single Company
    def finstate_all(self, corp, bsns_year, reprt_code='11011', fs_div='CFS'):
        corp_code = self.find_corp_code(corp)
        if not corp_code:
            raise ValueError(f'could not find "{corp}"')
        return dart_finstate.finstate_all(self.api_key, corp_code, bsns_year, reprt_code=reprt_code, fs_div=fs_div)

    #3-5. Accounts - XBRL
    def xbrl_taxonomy(self, sj_div):
        return dart_finstate.xbrl_taxonomy(self.api_key, sj_div=sj_div)

    #4. Shares
    #4-1. Shares - Mass Amount Ownership Report
    def major_shareholders(self, corp):
        corp_code = self.find_corp_code(corp)
        if not corp_code:
            raise ValueError(f'could not find "{corp}"')
        return dart_share.major_shareholders(self.api_key, corp_code)
    
    #5. Major Issues to Report
    def event(self, corp, key_word, start=None, end=None):
        corp_code = self.find_corp_code(corp)
        if not corp_code:
            raise ValueError(f'could not find "{corp}"')
        return dart_event.event(self.api_key, corp_code, key_word, start, end)
    
    #6. Share Report Forms
    def regstate(self, corp, key_word, start=None, end=None):
        corp_code = self.find_corp_code(corp)
        if not corp_code:
            raise ValueError(f'could not find "{corp}"')
        return dart_regstate.regstate(self.api_key, corp_code, key_word, start, end)
    
    #7. Utils
    #utils: list_date - all reports on a specific date (deprecated)
    def list_date(self, date=None, final=True, cache=True):
        warnings.warn('list_date() is deprecated. Use list_date_ex()')
    
    #utils: list_date_ex - dataframe of all reports on a specific date - inclues time
    def list_date_ex(self, date=None, cache=True):
        return dart_utils.list_date_ex(date, cache=cache)
    
    #utils: attach document list - dataframe of attached document list - title and URL
    def attach_doc_list(self, s, match=None):
        return dart_utils.attach_doc_list(s, match=match)

    #utils: subdocument list - dataframe of subdocument list - title and URL
    def sub_docs(self, s, match=None):
        return dart_utils.sub_docs(s, match=match)
    
    #utils: attach files file list - dataframe
    def attach_files(self, s):
        return dart_utils.attach_files(s)
    
    #utils: attach files file list - dataframe
    def attach_file_list(self, s):
        print('attach_file_list() will deprecated. Use attach_files() instead')
        return dart_utils.attach_files(s)
    
    #utils: save url as fn
    def download(self, url, fn):
        return dart_utils.download(url, fn)

    def retrieve(self, url, fn):
        print('retrieve() will deprecated. Use download() instead')
        return dart_utils.download(url, fn)


docs_cache_dir = 'docs_cache'
fn = 'opendartreader_corp_codes_{}.pkl'.format(datetime.today().strftime('%Y%m%d'))
fn_cache = os.path.join(docs_cache_dir, fn)
print(docs_cache_dir)
print(fn)
print(fn_cache)
