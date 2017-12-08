# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from langdetect import detect_langs
from scrapy.linkextractors import LinkExtractor
import json
import codecs

class JournalistSpider(scrapy.Spider):
    name = 'journalist' #Name of the spider
    start_urls = ['https://membres.fpjq.org/index.php?vMenu=153&amp;vOptions=Membres'] #site we try to scrape
    
    def parse(self, response):
        request = scrapy.FormRequest.from_response(
            response,
            formname='recherche',
            formdata={'Prenom': 'z'},
            callback=self.parse_recherche
            )
        print(request.body)
        yield request
        
    def parse_recherche(self,response):
        soup = BeautifulSoup(response.body, "html.parser")
        all_regular_infos = soup.findAll("table",{'style':"width:90%; margin-top:7px;"})
        all_extra_infos = soup.findAll("div",{'class':"fiche"})
        
        file = open('test.html',"w",encoding='utf8')
        for extra_infos in all_extra_infos:
            extra_infos = list(filter(None,extra_infos.text.splitlines()))
            #The number of tag is variable but it always follow the following pattern:
            #Tag_:Value  where _ = space
            tags = []
            values = []
            for line in extra_infos:
                line = line.split(' :')
                tags.append(line[0])
                values.append(line[1])
            print(tags)
                
                
            
            
        #Here we extract all the regular infor from the journalist
        for infos in all_regular_infos:
            infos = filter(infos.text.splitlines())
            
            #Here we get the first and last name
            full_name = infos[0].split(', ')
            last_name = full_name[0]
            first_name = full_name[1]
            
            #Here we get the occupation and journal (if any)
            occupation = infos[1]
            journal = infos[2]
            
            
            
        file.close()
        #print(regular_info)