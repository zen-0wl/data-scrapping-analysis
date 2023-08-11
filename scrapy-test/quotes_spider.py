import scrapy
import csv

class QuoteSpider(scrapy.Spider):
    name = 'quote-spider'
    start_urls = ['http://quotes.toscrape.com']
    
    quotes = []

    def parse(self, response):
        for quote in response.css('div.quote'):
            self.quotes.append({
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            })

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

    def closed(self, reason):
        self.save_to_csv()

    def save_to_csv(self):
        with open('quotes.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['text', 'author', 'tags']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(self.quotes)