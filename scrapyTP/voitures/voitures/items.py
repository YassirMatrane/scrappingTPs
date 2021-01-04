# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy
class VoituresItem(scrapy.Item):
    prix = scrapy.Field()
    Annee_Modele = scrapy.Field()
    Kilometrage = scrapy.Field()
    TypeDeCarburant = scrapy.Field()
    Marque = scrapy.Field()
    Modele = scrapy.Field()
    Puissance_fiscale = scrapy.Field()
    Type = scrapy.Field()
