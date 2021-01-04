import scrapy
import re
from voitures.items import VoituresItem
class VoituresSpider(scrapy.Spider):
    name = "voitures"
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

            if(prix==None):
                print('okokokokokokokokfokfokfokfofkofkofkfokwoooooooooowWWOOOOWWWOWOWO')
            else:
                print('le typeeeeeeeeeeeeeeee'+type(prix))
        except AttributeError:
            prix=0.0
        item = VoituresItem()
        item['prix']=prix,
        item['Annee_Modele']=response.css("div.span8 a::text")[0].extract(),
        item['Kilometrage']=response.css("div.span8 h2::text")[2].extract()[1:],
        item['TypeDeCarburant']=response.css("div.span8 a::text")[1].extract(),
        item['Marque']=response.css("div.span8 a::text")[2].extract(),
        item['Modele']=response.css("div.span8 a::text")[3].extract(),
        item['Puissance_fiscale']=response.css("div.span8 a::text")[4].extract(),
        item['Type']=response.css("div.span8 a::text")[5].extract()
        yield item

### scrapy crawl voitures -o s.csv
