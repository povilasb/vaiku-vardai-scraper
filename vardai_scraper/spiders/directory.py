import scrapy
from scrapy import Request


class NameUrl(scrapy.Item):
    url = scrapy.Field()


class NameDirectorySpider(scrapy.Spider):
    name = 'Names Directory Spider'
    start_urls = ['https://www.tevu-darzelis.lt/vaiku-vardai/']
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'Z',]

    def parse(self, response: scrapy.http.Response) -> None:
        ensure_response_200(response)
        for letter in self.letters:
            yield scrapy.Request(
                dir_url_for_letter(letter),
                callback=self.parse_index_page,
                meta={'letter': letter, 'curr_page': 1},
            )

    def parse_index_page(self, resp: scrapy.http.Response) -> None:
        ensure_response_200(resp)
        names = resp.xpath(
            '//ul[@class = "name-list"]/li/a/@href').extract()
        for name_url in names:
            yield NameUrl(url=resp.urljoin(name_url))

        page_count = extract_page_count(resp)
        curr_page = resp.meta['curr_page']
        if curr_page < page_count:
            curr_letter = resp.meta['letter']
            yield Request(
                dir_url_for_letter(curr_letter, curr_page + 1),
                callback=self.parse_index_page,
                meta={'letter': curr_letter, 'curr_page': curr_page + 1},
            )


def extract_page_count(resp: scrapy.http.Response) -> int:
    pages = resp.xpath('//ul[@class="pagination"]/li/a//text()')\
        .extract()
    pages = [safe_to_int(p) for p in pages]
    return max(pages)


def ensure_response_200(response: scrapy.http.Response) -> None:
    if response.status != 200:
        raise Exception('Expected HTTP response 200')


def dir_url_for_letter(letter: str, page_nr: int=1) -> str:
    url = f'https://www.tevu-darzelis.lt/vaiku-vardai/{letter}/'
    if page_nr > 1:
        url += f'?letter={letter}&page={page_nr}'
    return url


def safe_to_int(string: str, default_val: int=-1) -> int:
    try:
        return int(string)
    except ValueError:
        return default_val
