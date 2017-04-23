from typing import List, Tuple
import json

import scrapy
from scrapy import Request


class NameInfo(scrapy.Item):
    name = scrapy.Field()
    gender = scrapy.Field()
    origin = scrapy.Field()
    name_day = scrapy.Field()
    stats = scrapy.Field()


class NamePageSpider(scrapy.Spider):
    name = 'Names Page Spider'

    def start_requests(self) -> List[Request]:
        urls = read_name_urls_from('name_urls.json')
        return [Request(url, callback=self.parse_name_page) for url in urls]

    def parse_name_page(self, resp: scrapy.http.Response) -> None:
        ensure_response_200(resp)
        name, gender = extract_name(resp)

        info = resp.xpath('//div[@id="name-info"]/p//text()').extract()
        name_origin = info[1].strip()
        name_day = info[3].strip()

        years = resp.xpath('//div[@id="chart"]//text()')\
            .re_first('categories: \[(.*)\]')
        years = years.replace('"', '')
        years = [int(y) for y in years.split(',')]

        name_count = resp.xpath('//div[@id="chart"]//text()')\
            .re_first('data: \[(.*)\]')
        name_count = [int(cnt) for cnt in name_count.split(',')]

        yield NameInfo(
            name=name,
            gender=gender,
            origin=name_origin,
            name_day=name_day,
            stats=name_count,
        )

def ensure_response_200(response: scrapy.http.Response) -> None:
    if response.status != 200:
        raise Exception('Expected HTTP response 200')


def extract_name(resp: scrapy.http.Response) -> Tuple[str, str]:
    """
    Returns:
        (name, gender)
    """
    name = resp.xpath('//div[@id="page-left"]//h1[@class="boy"]//text()')\
        .extract_first()
    if name:
        return name, 'male'
    name = resp.xpath('//div[@id="page-left"]//h1[@class="girl"]//text()')\
        .extract_first()
    if name:
        return name, 'female'

    raise Exception('Failed to extract name')


def read_name_urls_from(fname: str) -> List[str]:
    data = read_json_from(fname)
    return [item['url'] for item in data]


def read_json_from(fname: str) -> dict:
    with open(fname, 'r') as f:
        return json.load(f)
