# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import csv
from langdetect import detect_langs
from scrapy.linkextractors import LinkExtractor
import json
import codecs

class media:
    def __init__(self):
        nom = ""
        type = "" 
        categorie = ""
        attr = []
        vals = []
        
class MediaSpider(scrapy.Spider):
    name = 'media' #Name of the spider
    start_urls = ['https://membres.fpjq.org/index.php?vMenu=153&vOptions=Medias'] #site we try to scrape
    def parse(self, response):
        request = scrapy.FormRequest.from_response(
            response,
            formname='recherche',
            formdata={'Nom': 'z'},
            callback=self.parse_recherche
            )
        print(request.body)
        yield request
        
    def parse_recherche(self,response):
        all_tags = set();
        medias = []
        tag_value_dict = []    
    
        soup = BeautifulSoup(response.body, "html.parser")
        all_regular_infos = soup.findAll("table",{'style':"width:90%; margin-top:7px;"})
        all_extra_infos = soup.findAll("div",{'class':"fiche"})
       
        file = open('test.html',"w",encoding='utf8')
        
        #TODO Do the same thing as in journalist_spiders but adapt items
        #Almost same format as before
        
        file.close()
