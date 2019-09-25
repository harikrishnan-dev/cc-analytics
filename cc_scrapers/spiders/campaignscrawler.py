# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from datetime import datetime as dt
from urllib.parse import urlparse


class CampaignscrawlerSpider(Spider):
    name = 'campaignscrawler'
    start_urls = ['https://www.ishaoutreach.org/en/cauvery-calling/campaigns//']
    pagination = 0
    storage = 'raw_links'

    def parse(self, response):
        campaign_urls = set(response.xpath('//article/a/@href').extract())
        if self.pagination>3:
            return
        for url in campaign_urls:
            yield {
                'link': url,
                'crawled_at': dt.utcnow().isoformat(),
                'storage': self.storage
            }

        header = { 'Host': urlparse(response.url).hostname, 'Referer': response.url}
        self.pagination = self.pagination+1
        url = 'https://www.ishaoutreach.org/en/cauvery-calling/campaigns/{params}'
        formdata = {'page_offset': self.pagination}

        url = url.format(params='?data%5Bcampaign_type%5D=&data%5Bsort_by%5D=end_date&data%5Bsearch_name%5D=&data%5Bpage_offset%5D='+str(self.pagination))
        yield Request(url=url,
            headers=header,
            method='GET',
            callback=self.parse, dont_filter=True
        )
