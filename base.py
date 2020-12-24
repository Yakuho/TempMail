from requests.utils import cookiejar_from_dict
from requests import Session
from json.decoder import JSONDecodeError
from json import loads
from lxml.etree import HTML
from time import time
from config import autoRetry
from config import timeout


class Mail:
    def __init__(self):
        self.session = Session()
        self.mailbox = str()
        self.cookie = dict()
        self.rear = str()
        self.address = list()
        self.message_status = list()
        self.message_box = list()
        self.session.cookies = cookiejar_from_dict(self.cookie)
        self.initial()

    @autoRetry
    def doc(self):
        """获取后缀名"""
        url = 'https://linshiyouxiang.net/'
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;'
                      'q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://linshiyouxiang.net/',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36',
        }
        self.session.headers = headers
        response = self.session.get(url, timeout=timeout)
        if response.status_code == 200:
            context = HTML(response.text)
            self.address = context.xpath('//*/ul[@class="dropdown-menu dropdown-menu-right"]/li/a/@data-mailhost')
            if self.address:
                return True
            else:
                return False
        else:
            return None

    @autoRetry
    def refresh(self, init=None, new_mail=None):
        """
        刷新邮箱消息
        :param init: 初始化(默认不初始化)
        :param new_mail: 刷新邮箱用户名(默认不刷新)
        :return:
        """
        url = 'https://linshiyouxiang.net/api/v1/mailbox/keepalive?'
        if init:
            parameters = {'mailbox': ''}
        elif new_mail:
            parameters = {'force_change': '1', '_ts': round(time() * 1000)}
        else:
            parameters = None
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://linshiyouxiang.net/',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.session.headers = headers
        response = self.session.request(method='get', url=url, params=parameters, timeout=timeout)
        if response.status_code == 200:
            try:
                data = loads(response.text)
                self.mailbox = data['mailbox']
                return True
            except JSONDecodeError:
                return None
        else:
            return None

    @autoRetry
    def message(self, mailbox=None):
        """读取邮箱消息"""
        if mailbox:
            url = f'https://linshiyouxiang.net/api/v1/mailbox/{mailbox}'
        else:
            url = f'https://linshiyouxiang.net/api/v1/mailbox/{self.mailbox}'
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://linshiyouxiang.net/',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.session.headers = headers
        response = self.session.request(method='get', url=url, timeout=timeout)
        if response.status_code == 200:
            try:
                data = loads(response.text)
                self.message_box = data
                self.message_status = [0] * len(data)
                return True
            except JSONDecodeError:
                return None
        else:
            return None

    @autoRetry
    def context(self, message_id=None):
        """读取某个消息的全文"""
        url = f'https://linshiyouxiang.net/mailbox/{self.mailbox}/{message_id}'
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;'
                      'q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://linshiyouxiang.net/',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/87.0.4280.88 Safari/537.36',
        }
        self.session.headers = headers
        response = self.session.request(method='get', url=url, timeout=timeout)
        print(url)
        if response.status_code == 200:
            context = HTML(response.text)
            return '\n'.join(context.xpath('//*/div[@class="mail-content"]/text()')).strip()
        else:
            return None

    @autoRetry
    def delete_message(self, message_id=None):
        """删除该条消息"""
        url = f'https://linshiyouxiang.net/api/v1/mailbox/{self.mailbox}/{message_id}'
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'origin': 'https://linshiyouxiang.net',
            'pragma': 'no-cache',
            'referer': f'https://linshiyouxiang.net/mailbox/3cp_lanv/{message_id}',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.session.headers = headers
        response = self.session.request(method='delete', url=url, timeout=timeout)
        if response.status_code == 200:
            return True
        else:
            return None

    def initial(self):
        print('邮箱站初始化中...')
        self.doc()
        if len(self.address):
            print(f'成功获取{len(self.address)}个不同地址')
        else:
            print('初始化失败! 没有获得任何邮箱地址')
            return False
        self.refresh(init=1)
        if self.mailbox:
            print(f'初始化完成!')
        else:
            print('初始化失败! 没有获得邮箱')
            return False


