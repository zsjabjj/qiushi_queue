# -*- coding: utf-8 -*-
import json
import threading

from lxml import etree
import requests
from queue import Queue


class Qiushi(object):
    '''使用多线程获取数据, 用到队列queue存放需要执行的操作'''
    def __init__(self):
        # 构建url
        self.url = 'https://www.qiushibaike.com/8hr/page/{}/'
        self.url_list = None
        # 构建headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }

        # 保存数据文件
        self.f = open('qiushi.json', 'w', encoding='UTF-8')

        # 创建存放需要执行操作的事件
        self.url_queue = Queue()
        self.resp_queue = Queue()
        self.data_queue = Queue()

    def __del__(self):
        self.f.close()

    def generate_url_list(self):
        # self.url_list = [self.url.format(i) for i in range(1, 14)]
        for i in range(1, 14):
            self.url_queue.put(self.url.format(i))

    def get_data(self):
        while self.url_queue.not_empty:
            url = self.url_queue.get()
            resp = requests.get(url, headers=self.headers)
            self.resp_queue.put(resp.content)
            # return resp.content
            self.url_queue.task_done()

    def parse_data(self):
        while self.resp_queue.not_empty:
            data = self.resp_queue.get()
            html = etree.HTML(data)
            node_list = html.xpath('//div[contains(@id, "qiushi_tag_")]')
            # print(len(node_list))
            # 获取数据
            data_list = list()

            for node in node_list:
                temp = dict()
                try:
                    temp['user'] = node.xpath('./div[1]/a[2]/h2/text()')[0].strip()  # strip 去除字符串两边的空白字符
                    temp['link'] = 'https://www.qiushibaike.com' + node.xpath('./div[1]/a[2]/@href')[0]
                    temp['gender'] = node.xpath('./div[1]/div/@class')[0].split(' ')[-1].replace('Icon', '')
                    temp['age'] = node.xpath('./div[1]/div/text()')[0]
                except:
                    temp['user'] = node.xpath('./div[1]/span[2]/h2/text()')[0]
                    temp['link'] = None
                    temp['gender'] = None
                    temp['age'] = None
                data_list.append(temp)
            self.data_queue.put(data_list)
            self.resp_queue.task_done()
            # return data_list

    def save_data(self):
        while self.data_queue.not_empty:
            data_list = self.data_queue.get()
            for data in data_list:
                data_str = json.dumps(data, ensure_ascii=False) + ',\n'
                self.f.write(data_str)
            self.data_queue.task_done()

    def run(self):
        # # 生成url列表
        # self.generate_url_list()
        # # 遍历url, 发送请求, 获取响应
        # for url in self.url_list:
        #     resp_data = self.get_data(url)
        #     # 解析数据
        #     resp_list = self.parse_data(resp_data)
        #     # 保存数据
        #     self.save_data(resp_list)

        # 创建存储线程的列表
        thread_list = list()

        # 创建生成url线程
        t_url = threading.Thread(target=self.generate_url_list)
        thread_list.append(t_url)

        # 创建获取数据的线程
        for i in range(3):
            t_data = threading.Thread(target=self.get_data)
            thread_list.append(t_data)

        # 创建解析数据的线程
        for i in range(3):
            t_parse = threading.Thread(target=self.parse_data)
            thread_list.append(t_parse)

        # 创建保存数据的线程
        t_save = threading.Thread(target=self.save_data)
        thread_list.append(t_save)

        # 开启线程
        for t in thread_list:
            # 守护线程的方式
            t.setDaemon(True)
            t.start()

        # 等待子线程结束
        self.url_queue.join()
        self.resp_queue.join()
        self.data_queue.join()


if __name__ == '__main__':
    qiushi = Qiushi()
    qiushi.run()
