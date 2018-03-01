# -*- coding: utf-8 -*-
import json

from lxml import etree

import requests


class Qiushi(object):
    def __init__(self):
        # 构建url
        self.url = 'https://www.qiushibaike.com/8hr/page/{}/'
        # 构建headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }

        # 保存数据文件
        self.f = open('qiushi.json', 'w', encoding='UTF-8')

    def __del__(self):
        self.f.close()

    def generate_url_list(self):
        self.url_list = [self.url.format(i) for i in range(1, 14)]

    def get_data(self, url):
        resp = requests.get(url, headers=self.headers)
        return resp.content

    def parse_data(self, data):
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
        return data_list

    def save_data(self, data_list):
        for data in data_list:
            data_str = json.dumps(data, ensure_ascii=False) + ',\n'
            self.f.write(data_str)

    def run(self):
        # 生成url列表
        self.generate_url_list()
        # 遍历url, 发送请求, 获取响应
        for url in self.url_list:
            resp_data = self.get_data(url)
            # 解析数据
            resp_list = self.parse_data(resp_data)
            # 保存数据
            self.save_data(resp_list)





if __name__ == '__main__':
    qiushi = Qiushi()
    qiushi.run()
