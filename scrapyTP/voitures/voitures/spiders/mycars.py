import scrapy
import re
import time
from scrapy.crawler import CrawlerProcess
class VoituresSpider(scrapy.Spider):
    name = "cars"
    start_urls = [
        'https://www.avito.ma/fr/maroc/voiture--%C3%A0_vendre',
    ]
    i=1
    def parse(self, response):
        urls=response.css("h2.fs14>a::attr(href)").extract()
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse_details)
        self.__class__.i+=1
        next_page = 'https://www.avito.ma/fr/maroc/voiture--%C3%A0_vendre?o='+str(self.__class__.i)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
    def xstr(self,s):
        if s is None:
            return ''
        return str(s)
    def parseNumber(self,value, as_int=False):
        a=self.xstr(value)
        try:
            number = float(re.sub('[^.\-\d]', '', a))
            if as_int:
                return int(number)
            else:
                return number
        except ValueError:
            return float('NaN')
    def parse_details(self,response):
        try:
            prix=self.parseNumber(response.css("span.amount::text").extract_first())
            annee=int(self.parseNumber(response.css("div.span8 a::text")[0].extract()))
        except AttributeError:
            prix=0.0
            annee=0
        item={
            'prix':prix,
            'Ann':annee,
            'Kilomtrage':response.css("div.span8 h2::text")[2].extract()[1:],
            'TypeDeCarburant':response.css("div.span8 a::text")[1].extract(),
            'Marque':response.css("div.span8 a::text")[2].extract(),
            'Modele':response.css("div.span8 a::text")[3].extract(),
            'Puissance fiscale':response.css("div.span8 a::text")[4].extract(),
            'type':response.css("div.span8 a::text")[5].extract()
            }
        yield item
