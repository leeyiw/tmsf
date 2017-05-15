import scrapy

from tmsf.items import HouseItem


class HousePriceSpider(scrapy.Spider):
    name = "house_price"

    def start_requests(self):
        urls = [
            'http://xs.hzfc365.com/index.jsp'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for row in response.xpath("//div[@id='s1']//tr"):
            item = HouseItem()
            item['name'] = row.xpath('td[1]/a/text()').extract_first().strip()
            item['signed'] = int(self.parse_digits(row.xpath('td[2]/span')))
            item['reserved'] = int(self.parse_digits(row.xpath('td[3]/span')))
            item['area'] = float(self.parse_digits(row.xpath('td[4]/span')))
            item['price'] = float(self.parse_digits(row.xpath('td[5]/span')))
            yield item

    def parse_digits(self, span_list):
        cls_digit_dict = {
            'numbzero': '0',
            'numbone': '1',
            'numbtwo': '2',
            'numbthree': '3',
            'numbfour': '4',
            'numbfive': '5',
            'numbsix': '6',
            'numbseven': '7',
            'numbeight': '8',
            'numbnine': '9',
            'numbdor': '.'
        }
        digits_s = ''
        for span in span_list:
            cls = span.xpath('@class').extract_first()
            digit_s = cls_digit_dict[cls]
            digits_s += digit_s
        return digits_s
