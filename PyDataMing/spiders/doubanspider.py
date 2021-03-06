# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from PyDataMing.items import PydatamingItem
import json
from PyDataMing.ShowJson import showJson

class Douban(CrawlSpider):

    name = "douban"
    redis_key = 'douban:start_urls'
    start_urls = ['http://bbs.52waha.com/thread-296146-5-1.html']

    url = 'http://bbs.52waha.com/thread-296146-5-1.html'

    def parse(self, response):
        # 源字典
        dict = {'post': '', 'replys': ''}
        # 定义 post 内部数据
        post = {}
        # 定义 replys 内部数据,列表  形式    ，循环把字典放入这里
        #replys = []


        selector = Selector(response)

        # 标题筛选
        tit = selector.xpath('//span[@id="thread_subject"]/text()').extract()
        if tit:
            titl = "".join(tit)
        else:
            tit = selector.xpath('//*[@id="thread_subject"]/text()').extract()
        if tit:
            titl = "".join(tit)
        else:
            tit = selector.xpath('//div[@class="bbs-title"]/h2/text()').extract()
        if tit:
            titl = "".join(tit)
        else:
            tit = selector.xpath('//*[ @ id = "consnav"] / span[4]/text()').extract()
        if tit:
            titl = "".join(tit)
        else:
            tit = selector.xpath('//*[@class="tit"]/h2/text()').extract()
        if tit:
            titl = "".join(tit)
        else:
            tit = selector.xpath('//*[@id="subject_tpc"]/text()').extract()
        if tit:
            titl = "".join(tit)



        print '标题',titl



        # 时间数据筛选
        tim = selector.xpath('//em[starts-with(@id,"authorposton")]/text()').extract()
        if tim:
            time = "".join(tim[0])
        else:
            tim = selector.xpath('// *[ @ class = "bbs-list"] / div[2] / div[1] / span[1]/text()').extract()
        if tim:
            time = "".join(tim[0])
        else:
            tim = selector.xpath('//*[@xname="date"]/text()').extract()
        if tim:
            time = "".join(tim[0])
        else:
            tim = selector.xpath('//*[@class="article_foot"]/span/text()').extract()
        if tim:
            time = "".join(tim[0])
        else:
            tim = selector.xpath('//*[@class="floot_right"]/div[1]/span[2]/text()').extract()
        if tim:
            time = "".join(tim[0])
        else:
            tim = selector.xpath('//*[@id="my_info_d"]/text()').extract()
            temp = selector.xpath('//*[@class="my_xiangqing_shijian"]/text()').extract()
            tim.extend(temp)
            # 合并列表
        if tim:
            time = "".join(tim[0])



        # content数据筛选
        data = selector.xpath('//div[@class="t_fsz"]/table/tr/td[@class="t_f"]')
        con = data.xpath('string(.)').extract()
        if data:
            cont = "".join(con[0])
        else:
            data = selector.xpath('//*[@class="bbs-list"]/div[2]/div[2]')
            con = data.xpath('string(.)').extract()
        if data:
            cont = "".join(con[0])
        else:
            #针对第四个 URL ，没抓到 post 内容
            data = selector.xpath('//*[@class="rconten"]/div[2]')
            con = data.xpath('string(.)').extract()
        if data:
            cont = "".join(con[0])
        else:
            data = selector.xpath('//*[@class="text"]')
            con = data.xpath('string(.)').extract()
        if data:
            cont = "".join(con[0])
        else:
            data = selector.xpath('//*[@class="tpc_content"]')
            con = data.xpath('string(.)').extract()
        if data:
            cont = "".join(con[0])
        else:
            data = selector.xpath('//*[@class= "t_f"]/font')
            con = data.xpath('string(.)').extract()
        if data:
            cont = "".join(con[0])



        # 作者模块搞定
        post['publish_date'] = time.strip()
        post['content'] = cont.strip()
        post['title'] = titl.strip()


        #循环把回复的 字典 添加进入 replys 列表中
        del tim[0]
        del con[0]

        print '回复个数',len(tim)
        i = 0

        replys = range(len(tim))


        while i < len(tim):
          replys[i] = {}
          replys[i]['publish_date'] = "".join(tim[i]).strip()
          replys[i]['content'] = "".join(con[i]).strip()
          replys[i]['title'] = titl.strip()
          i +=1

        dict['replys'] = replys
        dict['post'] = post

        #print dict
        showJson(dict)
