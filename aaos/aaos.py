# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from urllib.parse import urlparse
from socket import timeout
import re
import sys
import os
import json, csv, sys
import unicodedata
import codecs
from unicodedata import normalize
import xlsxwriter
import os.path
from http.cookiejar import CookieJar
import collections
import math

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

        
class Aggregator(object):
    
    def __init__(self, config):
        main_url, output_file = [config.get(k) for k in sorted(config.keys())]
        self.main_url = main_url
        self.output_file = output_file

    def request_to_page(self, url, state):
        try:
            """
            cookie_jar = CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
            urllib.request.install_opener(opener)

            # acquire cookie
            req = urllib.request.Request(url)
            rsp = urllib.request.urlopen(req)
            """
            
            params = urllib.parse.urlencode({
                'ctl00$TxtSearchTerm': '',
                'ctl00$mainContentPlaceHolder$RadioBtnListSearch':  'Location',
                'ctl00$mainContentPlaceHolder$RbtnUSSLocation':  'USA',
                'ctl00$mainContentPlaceHolder$DdlStateLocation':  state,
                'ctl00$mainContentPlaceHolder$TxtCity':  '',
                'ctl00$mainContentPlaceHolder$BtnSearch':  'Search',
                '__EVENTTARGET':  '',
                '__EVENTARGUMENT':  '',
                '__LASTFOCUS':  '',
                '__VIEWSTATE':  '/wEPDwUKMTkzNzgzMDI3MA9kFgJmDw8WAh4RU3ViTmFtZUxpdGVyYWxWYWwFE1BhdGllbnQgSW5mb3JtYXRpb25kFgICAw9kFgwCAQ8WBB4EVGV4dAW/AjxzY3JpcHQgdHlwZT0ndGV4dC9qYXZhc2NyaXB0Jz5BZFB1YmxpY1RvcCgpPC9zY3JpcHQ+PG5vc2NyaXB0PjxhIGhyZWY9J2h0dHA6Ly9hZC5kb3VibGVjbGljay5uZXQvanVtcC9hYW9zLm9yZy9GaW5kX2FuX09ydGhvcGFlZGlzdDtzej03Mjh4OTA7b3JkPTEyMzQ1Njc4OT8nIHRhcmdldD0nX2JsYW5rJyA+PGltZyBzcmM9J2h0dHA6Ly9hZC5kb3VibGVjbGljay5uZXQvYWQvYWFvcy5vcmcvRmluZF9hbl9PcnRob3BhZWRpc3Q7c3o9NzI4eDkwO29yZD0xMjM0NTY3ODk/JyBib3JkZXI9JzAnIGFsdD0nQWR2ZXJ0aXNlbWVudCcgLz48L2E+PC9ub3NjcmlwdD4eB1Zpc2libGVnZAIHDxYCHwEFVTxhIGhyZWY9J2h0dHBzOi8vZWJ1cy5hYW9zLm9yZy9kZWZhdWx0LmFzcHg/dGFiaWQ9MTY4JmFwcGxfY29kZT1BQU9TX0hPTUUnPkxvZyBJbjwvYT5kAgkPZBYCAgMPZBYCZg9kFgICAQ8PFgIfAmdkFgQCAw8WAh8CZ2QCBw9kFg4CAQ8WAh8CZ2QCBw8QZGQWAQIBZAIJDw8WAh8CaGQWAgINDxBkEBULATABNQIxMAIxNQIyMAIyNQIzMAIzNQI0MAI0NQI1MBULATABNQIxMAIxNQIyMAIyNQIzMAIzNQI0MAI0NQI1MBQrAwtnZ2dnZ2dnZ2dnZxYBZmQCCw8PFgIfAmdkFgQCBw8WAh8BBSRTdGF0ZTo8Zm9udCAgY2xhc3M9J2FsZXJ0Jz4qPC9mb250PiBkAgkPEA8WAh4LXyFEYXRhQm91bmRnZBAVPAwtLS1TZWxlY3QtLS0HQWxhYmFtYQZBbGFza2EOQW1lcmljYW4gU2Ftb2EHQXJpem9uYQhBcmthbnNhcwpDYWxpZm9ybmlhCENvbG9yYWRvC0Nvbm5lY3RpY3V0CERlbGF3YXJlFERpc3RyaWN0IG9mIENvbHVtYmlhHkZlZGVyYXRlZCBTdGF0ZXMgb2YgTWljcm9uZXNpYQdGbG9yaWRhB0dlb3JnaWEER3VhbQZIYXdhaWkFSWRhaG8ISWxsaW5vaXMHSW5kaWFuYQRJb3dhBkthbnNhcwhLZW50dWNreQlMb3Vpc2lhbmEFTWFpbmUQTWFyc2hhbGwgSXNsYW5kcwhNYXJ5bGFuZA1NYXNzYWNodXNldHRzCE1pY2hpZ2FuCU1pbm5lc290YQtNaXNzaXNzaXBwaQhNaXNzb3VyaQdNb250YW5hCE5lYnJhc2thBk5ldmFkYQ1OZXcgSGFtcHNoaXJlCk5ldyBKZXJzZXkKTmV3IE1leGljbwhOZXcgWW9yaw5Ob3J0aCBDYXJvbGluYQxOb3J0aCBEYWtvdGEXTm9ydGhlcm4gTWFyaW5hIElzbGFuZHMET2hpbwhPa2xhaG9tYQZPcmVnb24FUGFsYXUMUGVubnN5bHZhbmlhC1B1ZXJ0byBSaWNvDFJob2RlIElzbGFuZA5Tb3V0aCBDYXJvbGluYQxTb3V0aCBEYWtvdGEJVGVubmVzc2VlBVRleGFzEVVTIFZpcmdpbiBJc2xhbmRzBFV0YWgHVmVybW9udAhWaXJnaW5pYQpXYXNoaW5ndG9uDVdlc3QgVmlyZ2luaWEJV2lzY29uc2luB1d5b21pbmcVPAwtLS1TZWxlY3QtLS0CQUwCQUsCQVMCQVoCQVICQ0ECQ08CQ1QCREUCREMCRk0CRkwCR0ECR1UCSEkCSUQCSUwCSU4CSUECS1MCS1kCTEECTUUCTUgCTUQCTUECTUkCTU4CTVMCTU8CTVQCTkUCTlYCTkgCTkoCTk0CTlkCTkMCTkQCTVACT0gCT0sCT1ICUFcCUEECUFICUkkCU0MCU0QCVE4CVFgCVkkCVVQCVlQCVkECV0ECV1YCV0kCV1kUKwM8Z2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZGQCDQ9kFgICBQ8QDxYCHwNnZBAV9QEMLS0tU2VsZWN0LS0tC0FmZ2hhbmlzdGFuDUFsYW5kIElzbGFuZHMHQWxiYW5pYQdBbGdlcmlhDkFtZXJpY2FuIFNhbW9hB0FuZG9ycmEGQW5nb2xhCEFuZ3VpbGxhCkFudGFyY3RpY2ETQW50aWd1YSBBbmQgQmFyYnVkYQlBcmdlbnRpbmEHQXJtZW5pYQVBcnViYQlBdXN0cmFsaWEHQXVzdHJpYQpBemVyYmFpamFuB0JhaGFtYXMHQmFocmFpbgpCYW5nbGFkZXNoCEJhcmJhZG9zB0JlbGFydXMHQmVsZ2l1bQZCZWxpemUFQmVuaW4HQmVybXVkYQZCaHV0YW4HQm9saXZpYRZCb3NuaWEgQW5kIEhlcnplZ293aW5hCEJvdHN3YW5hDUJvdXZldCBJc2xhbmQGQnJhemlsGUJyaXRpc2ggSW5kaWFuIE9jZWFuIFRlcnIRQnJ1bmVpIERhcnVzc2FsYW0IQnVsZ2FyaWEMQnVya2luYSBGYXNvB0J1cnVuZGkIQ2FtYm9kaWEIQ2FtZXJvb24KQ2FwZSBWZXJkZQ5DYXltYW4gSXNsYW5kcxhDZW50cmFsIEFmcmljYW4gUmVwdWJsaWMEQ2hhZAVDaGlsZQVDaGluYRBDaHJpc3RtYXMgSXNsYW5kF0NvY29zIChLZWVsaW5nKSBJc2xhbmRzCENvbG9tYmlhB0NvbW9yb3MFQ29uZ28ZQ29uZ28tRGVtb2NyYXRpYyBSZXB1YmxpYwxDb29rIElzbGFuZHMKQ29zdGEgUmljYQxDb3RlIERJdm9pcmUHQ3JvYXRpYQRDdWJhBkN5cHJ1cw5DemVjaCBSZXB1YmxpYwdEZW5tYXJrCERqaWJvdXRpCERvbWluaWNhEkRvbWluaWNhbiBSZXB1YmxpYwpFYXN0IFRpbW9yB0VjdWFkb3IFRWd5cHQLRWwgU2FsdmFkb3IRRXF1YXRvcmlhbCBHdWluZWEHRXJpdHJlYQdFc3RvbmlhCEV0aGlvcGlhEEZhbGtsYW5kIElzbGFuZHMNRmFyb2UgSXNsYW5kcwRGaWppB0ZpbmxhbmQGRnJhbmNlFEZyYW5jZSwgTWV0cm9wb2xpdGFuDUZyZW5jaCBHdWlhbmEQRnJlbmNoIFBvbHluZXNpYRRGcmVuY2ggU291dGhlcm4gVGVycgVHYWJvbgZHYW1iaWEHR2VvcmdpYQdHZXJtYW55BUdoYW5hCUdpYnJhbHRhcgZHcmVlY2UJR3JlZW5sYW5kB0dyZW5hZGEKR3VhZGVsb3VwZQRHdWFtCUd1YXRlbWFsYQhHdWVybnNleQZHdWluZWENR3VpbmVhLUJpc3NhdQZHdXlhbmEFSGFpdGkYSGVhcmQgJiBNY2RvbmFsZCBJc2xhbmRzGEhvbHkgU2VlIChWYXRpY2FuIENpdHkgKQhIb25kdXJhcwlIb25nIEtvbmcHSHVuZ2FyeQdJY2VsYW5kBUluZGlhCUluZG9uZXNpYQRJcmFuBElyYXEHSXJlbGFuZAtJc2xlIG9mIE1hbgZJc3JhZWwFSXRhbHkHSmFtYWljYQVKYXBhbgZKZXJzZXkGSm9yZGFuCkthemFraHN0YW4FS2VueWEIS2lyaWJhdGkGS29zb3ZvBkt1d2FpdApLeXJneXpzdGFuGExhbyBQZW9wbGUgRGVtbyBSZXB1YmxpYwZMYXR2aWEHTGViYW5vbgdMZXNvdGhvB0xpYmVyaWEWTGlieWFuIEFyYWIgSmFtYWhpcml5YQ1MaWVjaHRlbnN0ZWluCUxpdGh1YW5pYQpMdXhlbWJvdXJnBU1hY2F1CU1hY2Vkb25pYQpNYWRhZ2FzY2FyBk1hbGF3aQhNYWxheXNpYQhNYWxkaXZlcwRNYWxpBU1hbHRhEE1hcnNoYWxsIElzbGFuZHMKTWFydGluaXF1ZQpNYXVyaXRhbmlhCU1hdXJpdGl1cwdNYXlvdHRlBk1leGljbxlNaWNyb25lc2lhLUZlZGVyYXRlZCBTdGF0FU1vbGRvdmEgLSBSZXB1YmxpYyBPZgZNb25hY28ITW9uZ29saWEKTW9udGVuZWdybwpNb250c2VycmF0B01vcm9jY28KTW96YW1iaXF1ZQdNeWFubWFyB05hbWliaWEFTmF1cnUFTmVwYWwLTmV0aGVybGFuZHMUTmV0aGVybGFuZHMgQW50aWxsZXMNTmV3IENhbGVkb25pYQtOZXcgWmVhbGFuZAlOaWNhcmFndWEFTmlnZXIHTmlnZXJpYQROaXVlDk5vcmZvbGsgSXNsYW5kC05vcnRoIEtvcmVhGE5vcnRoZXJuIE1hcmlhbmEgSXNsYW5kcwZOb3J3YXkET21hbghQYWtpc3RhbgVQYWxhdR9QYWxlc3RpbmlhbiBUZXJyaXRvcnksIE9jY3VwaWVkBlBhbmFtYRBQYXB1YSBOZXcgR3VpbmVhCFBhcmFndWF5BFBlcnULUGhpbGlwcGluZXMIUGl0Y2Fpcm4GUG9sYW5kCFBvcnR1Z2FsBVFhdGFyB1JldW5pb24HUm9tYW5pYRJSdXNzaWFuIEZlZGVyYXRpb24GUndhbmRhEFNhaW50IEJhcnRoZWxlbXkVU2FpbnQgS2l0dHMgQW5kIE5ldmlzC1NhaW50IEx1Y2lhDFNhaW50LU1hcnRpbgVTYW1vYQpTYW4gTWFyaW5vFVNhbyBUb21lIEFuZCBQcmluY2lwZQxTYXVkaSBBcmFiaWEHU2VuZWdhbAZTZXJiaWEKU2V5Y2hlbGxlcwxTaWVycmEgTGVvbmUJU2luZ2Fwb3JlCFNsb3Zha2lhCFNsb3ZlbmlhD1NvbG9tb24gSXNsYW5kcwdTb21hbGlhDFNvdXRoIEFmcmljYQ1Tb3V0aCBHZW9yZ2lhC1NvdXRoIEtvcmVhBVNwYWluCVNyaSBMYW5rYRlTdCBWaW5jZW50IEFuZCBHcmVuYWRpbmVzClN0LiBIZWxlbmEXU3QuIFBpZXJyZSBBbmQgTWlxdWVsb24FU3VkYW4IU3VyaW5hbWUYU3ZhbGJhcmQgJiBKYW4gTWF5ZW4gSXNsCVN3YXppbGFuZAZTd2VkZW4LU3dpdHplcmxhbmQUU3lyaWFuIEFyYWIgUmVwdWJsaWMGVGFpd2FuClRhamlraXN0YW4YVGFuemFuaWEtVW5pdGVkIFJlcHVibGljCFRoYWlsYW5kBFRvZ28HVG9rZWxhdQVUb25nYRNUcmluaWRhZCBBbmQgVG9iYWdvB1R1bmlzaWEGVHVya2V5DFR1cmttZW5pc3RhbhhUdXJrcyBBbmQgQ2FpY29zIElzbGFuZHMGVHV2YWx1EFUgUyBNaW5vciBJc2xhbmQGVWdhbmRhB1VrcmFpbmUUVW5pdGVkIEFyYWIgRW1pcmF0ZXMOVW5pdGVkIEtpbmdkb20HVXJ1Z3VheQpVemJla2lzdGFuB1ZhbnVhdHUJVmVuZXp1ZWxhB1ZpZXRuYW0YVmlyZ2luIElzbGFuZHMgKEJyaXRpc2gpGVdhbGxpcyBBbmQgRnV0dW5hIElzbGFuZHMOV2VzdGVybiBTYWhhcmEFWWVtZW4GWmFtYmlhCFppbWJhYndlFfUBDC0tLVNlbGVjdC0tLQNBRkcDQUxBA0FMQgNEWkEDQVNNA0FORANBR08DQUlBA0FUQQNBVEcDQVJHA0FSTQNBQlcDQVVTA0FVVANBWkUDQkhTA0JIUgNCR0QDQlJCA0JMUgNCRUwDQkxaA0JFTgNCTVUDQlROA0JPTANCSUgDQldBA0JWVANCUkEDSU9UA0JSTgNCR1IDQkZBA0JESQNLSE0DQ01SA0NQVgNDWU0DQ0FGA1RDRANDSEwDQ0hOA0NYUgNDQ0sDQ09MA0NPTQNDT0cDQ09EA0NPSwNDUkkDQ0lWA0hSVgNDVUIDQ1lQA0NaRQNETksDREpJA0RNQQNET00DVExTA0VDVQNFR1kDU0xWA0dOUQNFUkkDRVNUA0VUSANGTEsDRlJPA0ZKSQNGSU4DRlJBA0ZYWANHVUYDUFlGA0FURgNHQUIDR01CA0dFTwNERVUDR0hBA0dJQgNHUkMDR1JMA0dSRANHTFADR1VNA0dUTQNHR1kDR0lOA0dOQgNHVVkDSFRJA0hNRANWQVQDSE5EA0hLRwNIVU4DSVNMA0lORANJRE4DSVJOA0lSUQNJUkwDSU1OA0lTUgNJVEEDSkFNA0pQTgNKRVkDSk9SA0tBWgNLRU4DS0lSA0tPUwNLV1QDS0daA0xBTwNMVkEDTEJOA0xTTwNMQlIDTEJZA0xJRQNMVFUDTFVYA01BQwNNS0QDTURHA01XSQNNWVMDTURWA01MSQNNTFQDTUhMA01UUQNNUlQDTVVTA01ZVANNRVgDRlNNA01EQQNNQ08DTU5HA01ORQNNU1IDTUFSA01PWgNNTVIDTkFNA05SVQNOUEwDTkxEA0FOVANOQ0wDTlpMA05JQwNORVIDTkdBA05JVQNORksDUFJLA01OUANOT1IDT01OA1BBSwNQTFcDUFNFA1BBTgNQTkcDUFJZA1BFUgNQSEwDUENOA1BPTANQUlQDUUFUA1JFVQNST1UDUlVTA1JXQQNCTE0DS05BA0xDQQNNQUYDV1NNA1NNUgNTVFADU0FVA1NFTgNTUkIDU1lDA1NMRQNTR1ADU1ZLA1NWTgNTTEIDU09NA1pBRgNTR1MDS09SA0VTUANMS0EDVkNUA1NITgNTUE0DU0ROA1NVUgNTSk0DU1daA1NXRQNDSEUDU1lSA1RXTgNUSksDVFpBA1RIQQNUR08DVEtMA1RPTgNUVE8DVFVOA1RVUgNUS00DVENBA1RVVgNVTUkDVUdBA1VLUgNBUkUDR0JSA1VSWQNVWkIDVlVUA1ZFTgNWTk0DVkdCA1dMRgNFU0gDWUVNA1pNQgNaV0UUKwP1AWdnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnFgFmZAIPD2QWAgIbDxBkEBULATABNQIxMAIxNQIyMAIyNQIzMAIzNQI0MAI0NQI1MBULATABNQIxMAIxNQIyMAIyNQIzMAIzNQI0MAI0NQI1MBQrAwtnZ2dnZ2dnZ2dnZxYBZmQCEQ9kFgYCBw8WAh8BBSRTdGF0ZTo8Zm9udCAgY2xhc3M9J2FsZXJ0Jz4qPC9mb250PiBkAgkPEA8WAh8DZ2QQFTwMLS0tU2VsZWN0LS0tB0FsYWJhbWEGQWxhc2thDkFtZXJpY2FuIFNhbW9hB0FyaXpvbmEIQXJrYW5zYXMKQ2FsaWZvcm5pYQhDb2xvcmFkbwtDb25uZWN0aWN1dAhEZWxhd2FyZRREaXN0cmljdCBvZiBDb2x1bWJpYR5GZWRlcmF0ZWQgU3RhdGVzIG9mIE1pY3JvbmVzaWEHRmxvcmlkYQdHZW9yZ2lhBEd1YW0GSGF3YWlpBUlkYWhvCElsbGlub2lzB0luZGlhbmEESW93YQZLYW5zYXMIS2VudHVja3kJTG91aXNpYW5hBU1haW5lEE1hcnNoYWxsIElzbGFuZHMITWFyeWxhbmQNTWFzc2FjaHVzZXR0cwhNaWNoaWdhbglNaW5uZXNvdGELTWlzc2lzc2lwcGkITWlzc291cmkHTW9udGFuYQhOZWJyYXNrYQZOZXZhZGENTmV3IEhhbXBzaGlyZQpOZXcgSmVyc2V5Ck5ldyBNZXhpY28ITmV3IFlvcmsOTm9ydGggQ2Fyb2xpbmEMTm9ydGggRGFrb3RhF05vcnRoZXJuIE1hcmluYSBJc2xhbmRzBE9oaW8IT2tsYWhvbWEGT3JlZ29uBVBhbGF1DFBlbm5zeWx2YW5pYQtQdWVydG8gUmljbwxSaG9kZSBJc2xhbmQOU291dGggQ2Fyb2xpbmEMU291dGggRGFrb3RhCVRlbm5lc3NlZQVUZXhhcxFVUyBWaXJnaW4gSXNsYW5kcwRVdGFoB1Zlcm1vbnQIVmlyZ2luaWEKV2FzaGluZ3Rvbg1XZXN0IFZpcmdpbmlhCVdpc2NvbnNpbgdXeW9taW5nFTwMLS0tU2VsZWN0LS0tAkFMAkFLAkFTAkFaAkFSAkNBAkNPAkNUAkRFAkRDAkZNAkZMAkdBAkdVAkhJAklEAklMAklOAklBAktTAktZAkxBAk1FAk1IAk1EAk1BAk1JAk1OAk1TAk1PAk1UAk5FAk5WAk5IAk5KAk5NAk5ZAk5DAk5EAk1QAk9IAk9LAk9SAlBXAlBBAlBSAlJJAlNDAlNEAlROAlRYAlZJAlVUAlZUAlZBAldBAldWAldJAldZFCsDPGdnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZxYBZmQCDw8QDxYCHwNnZBAVCwwtLS1TZWxlY3QtLS0DQXJtBUVsYm93DkZvb3QgYW5kIEFua2xlDkhhbmQgYW5kIFdyaXN0A0hpcARLbmVlCExvdyBCYWNrBE5lY2sIU2hvdWxkZXIFU3BpbmUVCwwtLS1TZWxlY3QtLS0DQVJNBUVMQk9XBEZPT1QESEFORANISVAES05FRQVMQkFDSwRORUNLBVNITERSBVNQSU5FFCsDC2dnZ2dnZ2dnZ2dnFgFmZAILDxYEHwEF0wI8c2NyaXB0IHR5cGU9J3RleHQvamF2YXNjcmlwdCc+QWRQdWJsaWNSaWdodCgpPC9zY3JpcHQ+PG5vc2NyaXB0PjxhIGhyZWY9J2h0dHA6Ly9hZC5kb3VibGVjbGljay5uZXQvanVtcC9hYW9zLm9yZy9GaW5kX2FuX09ydGhvcGFlZGlzdDtzej0xMjB4NjAwLDE2MHg2MDA7b3JkPTEyMzQ1Njc4OT8nIHRhcmdldD0nX2JsYW5rJyA+PGltZyBzcmM9J2h0dHA6Ly9hZC5kb3VibGVjbGljay5uZXQvYWQvYWFvcy5vcmcvRmluZF9hbl9PcnRob3BhZWRpc3Q7c3o9MTIweDYwMCwxNjB4NjAwO29yZD0xMjM0NTY3ODk/JyBib3JkZXI9JzAnIGFsdD0nQWR2ZXJ0aXNlbWVudCcgLz48L2E+PC9ub3NjcmlwdD4fAmdkAhEPFgIeC18hSXRlbUNvdW50AhIWJGYPZBYEAgEPFgQfAQUQPGgzPkNNRTwvaDM+PHVsPh8CZ2QCAw8PFgYfAQUSTGVhcm5pbmcgUG9ydGZvbGlvHgtOYXZpZ2F0ZVVybAVAaHR0cDovL3d3dzcuYWFvcy5vcmcvRWR1Y2F0aW9uL21vY21hbmFnZXIvTGVhcm5pbmdQb3J0Zm9saW8uYXNweB8CZ2RkAgEPZBYCAgMPDxYGHwEFD0NvdXJzZSBDYWxlbmRhch8FBTNodHRwOi8vd3d3Ny5hYW9zLm9yZy9lZHVjYXRpb24vY291cnNlcy9jb3Vyc2VzLmFzcHgfAmdkZAICD2QWAgIDDw8WBh8BBRdPbmxpbmUgYW5kIERpZ2l0YWwgIENNRR8FBS1odHRwOi8vd3d3My5hYW9zLm9yZy9wcm9kdWN0L2RpZ2l0YWxtZWRpYS5jZm0fAmdkZAIDD2QWAgIDDw8WBh8BBQxFeGFtaW5hdGlvbnMfBQU+aHR0cDovL3d3dzcuYWFvcy5vcmcvZWR1Y2F0aW9uL2V4YW1pbmF0aW9uY2VudGVyL2V4YW10eXBlLmFzcHgfAmdkZAIED2QWAgIDDw8WBh8BBRRDb21tdW5pY2F0aW9uIFNraWxscx8FBS1odHRwOi8vd3d3My5hYW9zLm9yZy9lZHVjYXRpb24vY3NtcC9pbmRleC5jZm0fAmdkZAIFD2QWAgIDDw8WBh8BBQpUZWFtU1RFUFBTHwUFNWh0dHA6Ly93d3cuYWFvcy5vcmcvZWR1Y2F0aW9uL1RlYW1TVEVQUFMvdGVhbWhvbWUuYXNwHwJnZGQCBg9kFgICAw8PFgYfAQUPQ01FIFRyYW5zY3JpcHRzHwUFOGh0dHA6Ly93d3c3LmFhb3Mub3JnL21lbWJlci90cmFuc2NyaXB0cy90cmFuc2NyaXB0cy5hc3B4HwJnZGQCBw9kFgICAw8PFgYfAQUiTWFpbnRlbmFuY2Ugb2YgQ2VydGlmaWNhdGlvbiAoTU9DKR8FBS9odHRwOi8vd3d3My5hYW9zLm9yZy9lZHVjYXRpb24vbW9jL21vY19pbmZvLmNmbR8CZ2RkAggPZBYCAgMPDxYGHwEFDU1lbWJlciBBbGVydHMfBQU1aHR0cDovL3d3dzMuYWFvcy5vcmcvbWVtYmVyL3NhZmV0eS9wc21vL3BzbW9hbGVydC5jZm0fAmdkZAIJD2QWBgIBDxYEHwEFJzwvdWw+PGgzPk9ydGhvcGFlZGljIFJlc291cmNlczwvaDM+PHVsPh8CZ2QCAw8PFgYfAQUDT0tPHwUFLGh0dHA6Ly9vcnRob3BvcnRhbC5hYW9zLm9yZy9va28vZGVmYXVsdC5hc3B4HwJnZGQCBQ8WBB8BBSA8YnI+T3J0aG9wYWVkaWMgS25vd2xlZGdlIE9ubGluZR8CZ2QCCg9kFgICAw8PFgYfAQUFU3RvcmUfBQUpaHR0cDovL3d3dzMuYWFvcy5vcmcvcHJvZHVjdC9wcm9kdWN0cy5jZm0fAmdkZAILD2QWAgIDDw8WBh8BBSZDb21wbGV0ZWQgQ2xpbmljYWwgUHJhY3RpY2UgR3VpZGVsaW5lcx8FBTFodHRwOi8vd3d3LmFhb3Mub3JnL3Jlc2VhcmNoL2d1aWRlbGluZXMvZ3VpZGUuYXNwHwJnZGQCDA9kFgQCAQ8WBB8BBSA8L3VsPjxoMz5Bbm51YWwgTWVldGluZzwvaDM+PHVsPh8CZ2QCAw8PFgYfAQUOQW5udWFsIE1lZXRpbmcfBQUvaHR0cDovL3d3dy5hYW9zLm9yZy9lZHVjYXRpb24vYW5tZWV0L2FubWVldC5hc3AfAmdkZAIND2QWAgIDDw8WBh8BBRpGdXR1cmUgTWVldGluZyBJbmZvcm1hdGlvbh8FBS9odHRwOi8vd3d3LmFhb3Mub3JnL2VkdWNhdGlvbi9hbm1lZXQvYW5ubXRnLmFzcB8CZ2RkAg4PZBYCAgMPDxYGHwEFCEFyY2hpdmVzHwUFMWh0dHA6Ly93d3cuYWFvcy5vcmcvZWR1Y2F0aW9uL2FubWVldC9wcmV2bWVldC5hc3AfAmdkZAIPD2QWBAIBDxYEHwEFHzwvdWw+PGgzPkludGVybmF0aW9uYWw8L2gzPjx1bD4fAmdkAgMPDxYGHwEFCkFjdGl2aXRpZXMfBQU6aHR0cDovL3d3dy5hYW9zLm9yZy9lZHVjYXRpb24vaW50ZXJuYXRpb25hbC9hY3Rpdml0aWVzLmFzcB8CZ2RkAhAPZBYEAgEPFgQfAQUlPC91bD48aDM+UGF0aWVudCBJbmZvcm1hdGlvbjwvaDM+PHVsPh8CZ2QCAw8PFgYfAQURUGF0aWVudCBCcm9jaHVyZXMfBQUwaHR0cDovL3d3dzMuYWFvcy5vcmcvcHJvZHVjdC9wYXRpZW50YnJvY2h1cmUuY2ZtHwJnZGQCEQ9kFgICAw8PFgYfAQUNUGF0aWVudCBWaWRlbx8FBS1odHRwOi8vd3d3My5hYW9zLm9yZy9wcm9kdWN0L3BhdGllbnR2aWRlby5jZm0fAmdkZAIVDxYCHwEFBDIwMTVkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYDBSxjdGwwMCRtYWluQ29udGVudFBsYWNlSG9sZGVyJFJidG5VU1NMb2NhdGlvbgUsY3RsMDAkbWFpbkNvbnRlbnRQbGFjZUhvbGRlciRSYnRuQ2FuTG9jYXRpb24FLGN0bDAwJG1haW5Db250ZW50UGxhY2VIb2xkZXIkUmJ0bkNhbkxvY2F0aW9udpvwEhLZBo5MMlU4RoiyXx20zP8Fsd1xlH14dpkpx/k=',
                '__VIEWSTATEGENERATOR':  '75059634',
                '__EVENTVALIDATION':  '/wEdAErjEHn0V9BZ+uHIedbl6iWMY7wrTRSW4rx0XiQuxexk2rRWQ3gjC29ZJIM376XR7Gl3OKlCJAvo1xcnyjrgnsy/pku+iHe5UiT2IX8GU4n/Mht1RHMubDuxErZaO8RLxqvFKCGseL3jVNOo4QgCzj3dkt88VYwE32mclXxOZGWowa7CUJ80LLTnsoNVnl+5GDlZRJxs2u7a7/+VXxfSO5M8KN0D58acW2iBC/x3eY6xc0fop2yF9KKoX9taHmwyubUSZrBZfIvEeMJx51Ow3HMiFOf+NyoGDhHh2YFefzpjMaYOJd8uMwSK2/haHBogd5YUeE4lmmapUPa62+91RH+WHh2I9if76I0lG2BxsR4oVPyvt/zgVj0gNHe+EZLC1elyy1Iyhv7qcpNF1ZGJipzUwQEiDLOwyPQNLWz7m4fZyUihlRO5j0Zg3zg4cj0X5zsEnI0+OFSqvs/WbyY00jNAgz+0lGIqUKNtWGkXzkSpZlWqdakidYrrUz3Wxpl13zTYGFHtK/y2TctZoTfveJe7jgdw+tMKWutfgZKF/VGpkVB3aXVy05z3NyxVTmgmevglC5qOd1sTrZkGjIdStPm6lQlpUz65P+e1o/9bTmEbCVWkhUeVeOpiFgesKxdbX20MSmDjAZNXCeuhjI75kQiYiOMD35H//WSqvoVzBiP4lGPL9mKvEQuUC0vCRMD3rnojM6CeFjxQ3KGWf1g/urGAQVjHt94V0aNlPD9N1pp7D2XbkzNvvmKJ83hYhkBBaJkAYiwChUJKdPxxJTugAKTtKmwGRCaHwXQMf2ExsSWIaY5L+7pGWYMZnnGMY9Nc1DNZUUWZF7wbVnchLiJ3h0HOd4C8/DIGM0olKhTgBLV4l9Az/KYRS8HX+qasR+G+1LMkx42y1QKJbO0jsCcOpL+86rxsfK2kfoG6x/GSnWqQKa5Fwz5M6BthapdsPLAww1qcyBkiYlEcYZD7iRbJNkskvzAwfPlNfOxnKxgjrRpWF4mtcgsl8vntsLfZLN96RiTxnG4UapijWF3eSTTE30WeF17Sf+1s8VLOHTHgpUkXoAbYJ043iNUCZEFR3Gzojf5CtW2lHbbhIXUZ1FFjBaQJdcVSr9SdDSvyv3QfHihVCB2/0DBO9yrg7dY2Va9Mgh70CPRViWGC3aeQIgc6o5JXORTHV9yQqcuMtRqKQonHjyoiXBZv0HuEf9N3dT7IvDzV4V/pL0Y3xAhNw18llWrjtQfNsEnhS7iWWqZxjKr3uKEqRWVW6QcrGMvLS2cpltgy446GahNzs8DZocl59bJ+Ca9NV5MUEY/+O8tvXKSmQ3zBtiWyE3v+upf246x8b9j89hPRtStYdQNd5Lg15xxBduo6eXUXy1CfEn2+20XACMferpjYoabokQNNtjbU2iRBNdjHemKLZaQWTBKN42VwGltmyk8irmDhtOsF9Ta9U2s32AqzXpmNBaI3Jn4zWj0rUVQV9Fl0bTPGBS/SPlotnEq1cpd5swUlgxFi2J/+U+R4VyNAG1HpusqWvM4zsd6gWZUcrMXm3h2tuOe9iaRu5DCxFueTvjbbPg+NXbMdjQPfC/e+j8Jc+s7Rk7/IKnkIaWHvvUT5ZA7eljWaRmBn',
            })

            data = params.encode('utf-8')
            request = urllib.request.Request(url)
            request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
            request.add_header("Accept-Language","ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4")
            request.add_header("Cache-Control","max-age=0")
            request.add_header("Connection","keep-alive")
            request.add_header("Host","www7.aaos.org")
            request.add_header("Origin","http://www7.aaos.org")
            request.add_header("Referer","http://www7.aaos.org/member/directory/search.aspx?directory=public")
            request.add_header("User-Agent","Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36")
            request.add_header("X-Compress","null")
            request.add_header("Content-type","application/x-www-form-urlencoded")

            page = urllib.request.urlopen(request, data)
            content = page.read()
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                print('Failed to connect to server.')
                print('Reason: ', e.reason)
                print(current_url)
            elif hasattr(e, 'code'):
                print('Error code: ', e.code)
            sys.exit(1)
        except timeout:
            print('socket timed out - URL %s', current_url)
            
        return content

    def start_process(self):

        code_list = ['AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'VI', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
        on_page = 20
        result = []
        
        for state in code_list:
            
            print(self.main_url)
            content = self.request_to_page(self.main_url, state)
            soup = BeautifulSoup(content, "lxml")
            try:
                count_res = soup.findAll('div',  {"id": "ctl00_mainContentPlaceHolder_PanelSearchResults"})[0].findAll('div')
                count = count_res[1].text
                cnt = re.findall('^(.*?)'+re.escape('results.'), count, re.DOTALL)[0].strip()
                if(not cnt.isdigit()):
                   cnt = 0 
            except:
                cnt = 0

            num_pages = math.ceil(int(cnt)/on_page)

            
            for page_index in range(1,num_pages+1):
                page_index = page_index.__str__()
                content = self.request_to_page(self.main_url+'&page='+page_index, state)
                soup = BeautifulSoup(content, "lxml")
                table = soup.find('table')
                trs = table.findAll('tr')            
                title_list = trs[0::3]
                contacts_list = trs[1::3]
                num = len(title_list)
                for i in range(0,num):
                    
                    obj = {'name': '', 'status': '', 'site': '', 'adress': '', 'city': '', 'code': '', 'index': '', 'phone': '', 'fax': ''}
                    divs = title_list[i].findAll('div')
                    name = divs[0].text.strip()
                    obj['name'] = name
                    status = divs[1].text.replace('Member Status:','').strip()
                    obj['status'] = status
                    if(divs[2].text.strip() != ''):
                        site = divs[2].find('a').attrs['href'].strip()
                        obj['site'] = site
                    else:
                        site = ''

                    divr = contacts_list[i].findAll('div')
                    
                    for div in divr:
                        str = div.text.strip()
                        if(str.find('Office:') != -1):
                            full_adress = div.text.replace('Office:','').strip()
                            list_adress = full_adress.split('\n')
                            if(len(list_adress)>2):
                                adress = ' '.join(list_adress[:-1]).strip()
                                city_code = list_adress[-1].split(',')
                                city = city_code[0].strip()
                                try:
                                    code_index = city_code[1].strip().split(' ')
                                except:
                                    print(state, page_index, city_code)
                                    
                                if (code_index[0] in code_list):
                                    code = code_index[0]
                                else:
                                    code = ''
                                index = code_index[1]
                                obj['adress'] = adress
                                obj['city'] = city
                                obj['code'] = code
                                obj['index'] = index
                            else:
                                adress = list_adress[0].strip()
                                city_code = list_adress[1].split(',')
                                city = city_code[0].strip()
                                try:
                                    code_index = city_code[1].strip().split(' ')
                                except:
                                    print(state, page_index, city_code)    
                                if (code_index[0] in code_list):
                                    code = code_index[0]
                                else:
                                    code = ''
                                index = code_index[1]
                                obj['adress'] = adress
                                obj['city'] = city
                                obj['code'] = code
                                obj['index'] = index
                        else:
                            adress = ''
                            city = ''
                            code = ''
                            index = ''
                            
                            
                        if(str.find('Office Phone:') != -1): 
                            phone = div.text.replace('Office Phone:','').replace('\n','').strip()
                            obj['phone'] = phone
                        else:
                            phone = ''
                            
                        if(str.find('Fax:') != -1): 
                            fax = div.text.replace('Fax:','').replace('\n','').strip()
                            obj['fax'] = fax
                        else:
                            fax = ''
                        
                    result.append(obj)
                
        
        workbook = xlsxwriter.Workbook(self.output_file)
        worksheet_1 = workbook.add_worksheet()

        header_format = workbook.add_format({'bold': True,
                                             'align': 'center',
                                             'valign': 'vcenter',
                                             'fg_color': '#D7E4BC',
                                             'border': 1})

        main_format = workbook.add_format({'bold': False, 'text_wrap': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter'})
        title_format = workbook.add_format({'bold': False, 'text_wrap': 1, 'border': 1, 'valign': 'vcenter'})
                                             
        worksheet_1.set_column('A:A', 40)
        worksheet_1.set_column('B:B', 40)
        worksheet_1.set_column('C:C', 40)
        worksheet_1.set_column('D:D', 40)
        worksheet_1.set_column('E:E', 40)
        worksheet_1.set_column('F:F', 40)
        worksheet_1.set_column('G:G', 40)
        worksheet_1.set_column('H:H', 40)
        worksheet_1.set_column('I:I', 40)

        worksheet_1.write(0, 0, 'Name', header_format)
        worksheet_1.write(0, 1, 'Member Status', header_format)
        worksheet_1.write(0, 2, 'Website', header_format)
        worksheet_1.write(0, 3, 'Address', header_format)
        worksheet_1.write(0, 4, 'City', header_format)
        worksheet_1.write(0, 5, 'State', header_format)
        worksheet_1.write(0, 6, 'Zip', header_format)
        worksheet_1.write(0, 7, 'Phone', header_format)
        worksheet_1.write(0, 8, 'Fax', header_format)

        row = 1
        col = 0
        
        for obj in result:
            worksheet_1.set_row(row, 40)
            worksheet_1.write(row, 0, obj.get('name'), main_format)
            worksheet_1.write(row, 1, obj.get('status'), main_format)
            worksheet_1.write(row, 2, obj.get('site'), title_format)
            worksheet_1.write(row, 3, obj.get('adress'), main_format)
            worksheet_1.write(row, 4, obj.get('city'), main_format)
            worksheet_1.write(row, 5, obj.get('code'), title_format)
            worksheet_1.write(row, 6, obj.get('index'), main_format)
            worksheet_1.write(row, 7, obj.get('phone'), main_format)
            worksheet_1.write(row, 8, obj.get('fax'), title_format)
            row += 1


        workbook.close()
            
        
if __name__ == '__main__':
    settings = { 'main_url': 'http://www7.aaos.org/member/directory/search.aspx?directory=public', 'output_file': 'output.xlsx' }
    aggregator = Aggregator(settings)
    aggregator.start_process()