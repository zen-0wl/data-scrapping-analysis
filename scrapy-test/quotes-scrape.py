import scrapy

class QuoteSpider(scrapy.Spider):
    name = 'quote-spider'
    start_urls = ['http://quotes.toscrape.com/page/1/']

    def parse(self, response):
        QUOTE_SELECTOR = '.quote'
        TEXT_SELECTOR = '.text::text'
        AUTHOR_SELECTOR = '.author::text'
        TAGS_SELECTOR = '.tags .tag::text'

        for quote in response.css(QUOTE_SELECTOR):
            yield {
                'text': quote.css(TEXT_SELECTOR).get(),
                'author': quote.css(AUTHOR_SELECTOR).get(),
                'tags': quote.css(TAGS_SELECTOR).getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )