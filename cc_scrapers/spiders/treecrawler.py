# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from cc_scrapers.store.mongo import get_queries
import datetime as dt


class TreecrawlerSpider(Spider):
    name = 'treecrawler'
    start_urls = ['http://https://www.ishaoutreach.org/en/cauvery-calling/campaigns/cauvery-calling-karnataka-action-now-91/']

    def start_requests(self):
        l=get_queries()
        print("found records",l)
        for item in l:
            yield Request(item.get('link'))
            #print(item.get('link'))
        #yield


    def parse(self, response):
        # Parse scraped output

        # Sample input: 1,234
        tree_count = response.css('div.rs::text')[0].get()[:-5].replace(',', '').strip()

        # Sample input: 1 Lac
        pledge_goal = self.parse_indian_notation_to_number(response.css('div.subtext::text')[0].get()[17:-6])

        if not pledge_goal:
            return
        # Sample input: Tamil Nadu
        region = response.xpath('//div[@class="content1"]/div/text()').extract()[0]

        # Sample input: 1,234
        supporters_count = response.css('div.no::text')[0].get().replace(',', '').strip()

        # Sample input: 1,234
        fundraisers_count = response.xpath("//*[contains(text(), 'FUNDRAISERS (')]/text()").extract()[0][
                            17:-1].replace(',', '').strip()

        print("Region", region)
        print("tree donated", tree_count)
        # self.logger.info('Region - ' + region)
        # self.logger.info('\tPledge - ' + str(pledge_goal))
        # self.logger.info('\tTrees donated - ' + tree_count)
        # self.logger.info('\tSupporters - ' + supporters_count)
        # self.logger.info('\tFundraisers - ' + fundraisers_count)

        yield {
            'crawled_at': dt.datetime.utcnow().isoformat(),
            'region': region,
            'pledge': pledge_goal,
            'trees': tree_count,
            'supporters': supporters_count,
            'fundraisers': fundraisers_count,
            'storage': 'raw_data',
            'link': response.url
        }


    def parse_indian_notation_to_number(self, value: str):
        splitted = value.split(' ')
        if splitted and len(splitted)>1:
            if splitted[1] == 'Thousand':
                return int(value[0]) * 1000
            if splitted[1] == 'Lac':
                return int(value[0]) * 100000
            if splitted[1] == 'Crore':
                return int(value[0]) * 10000000
        
        return None