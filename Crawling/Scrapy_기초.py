# 필요하면 설치! / 그런데 일반저으로는 필요함, 설치하자.
# pip install scrapy
# pip install scrapyd
# pip install scrapyd-client

import scrapy

class NewsSpider(scrapy.Spider):
    name = "news"
    #allowed_domains = ["naver.com"]
    #start_urls = ["https://naver.com"]

    def start_requests(self):
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language':'ko,en;q=0.9,en-US;q=0.8',
            'Cache-Control':'max-age=0',
            'Cookie':'JSESSIONID=CDDF4C5B2CC3EFD18D4FFA2B02C1AF29; NNB=CHKVUBVG34SGK; isShownNewLnb=Y',
            'Sec-Ch-Ua':'"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'Sec-Ch-Ua-Mobile':'?0',
            'Sec-Ch-Ua-Platform':'"Windows"',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site':'none',
            'Sec-Fetch-User':'?1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
        }

        url = 'https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=005'
        yield scrapy.Request(url, callback=self.parse, headers=headers)

    def parse(self, response):
        print(response.text)