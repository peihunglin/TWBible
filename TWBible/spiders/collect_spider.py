import scrapy
import urllib
import json
import codecs

from scrapy.selector import Selector
from TWBible.items import TwbibleItem


class CollectSpider(scrapy.Spider):
    name = "collect"
    BASE_URL = 'https://bible.fhl.net'

    def start_requests(self):
        SUB_URL = '/new/read.php'
        params = {
            'VERSION80': 'ttvcl2021',
            'TABFLAG': 1,
            'chineses': '創',
            'chap': 1
        }
        url = f'{self.BASE_URL}{SUB_URL}/?{urllib.parse.urlencode(params)}'
        request = scrapy.Request(url, callback=self.parse)
        request.meta['params'] = params
        return [request]

    def parse(self, response):
        sel = Selector(response) 
        cururl = response.request.url
        print(cururl)
        yield scrapy.Request(cururl, callback=self.parse_table,dont_filter = True)
        nextch = sel.xpath("//a[@id='pnext']/@href").get()
        print("has next ch:" + str(nextch))
        if nextch:
            nexturl = f'{self.BASE_URL}/{nextch}'
            yield scrapy.Request(nexturl, callback=self.parse)
            

        
    def parse_table(self, response):
        sel = Selector(response) 
#        with open("dmp.txt", "w") as f:
#            f.write(response.text)
        book = sel.xpath("//body//font[@size='+2']/text()").get()
        unibook = book.encode("unicode_escape")
        #print(book)
        #print(unibook)

        for id, row in enumerate(sel.xpath("//table//tr")):
            if id == 0:
                continue
            cols = row.xpath("./td")
            #print(cols)
            vid = cols[0].xpath("./b/text()").get()
            #print(vid)
            chapterID = int(vid.split(":")[0])
            verseID = int(vid.split(":")[1])
            vcontent = str(cols[1].xpath("./text()").get())
            if vcontent == "None":
                #vcontent = str(cols[1].xpath("./span/text()").get())
                vcontent = str(cols[1].xpath("string()").extract())
                #print("vcontent",cols[1].xpath("string()").extract())
            univcontent = vcontent.encode("unicode_escape")
            #print("Book:"+ book +" chapter "+str(chapterID)+" verse:" +str(verseID))
            #print(cols[1])
            #print(univcontent)
            item = TwbibleItem()
            item['book'] = book
            #item['unibook'] = unibook
            item['chapterID'] = chapterID
            item['verseID'] = verseID
            item['verse'] = vcontent
            #item['universe'] = univcontent
            yield item
            #print(item)
