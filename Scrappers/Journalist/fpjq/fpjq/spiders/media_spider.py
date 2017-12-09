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
            formdata={'Nom': '_'},
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
        
        media_index = 0
        #Here we extract all the regular infor from the journalist
        for infos in all_regular_infos:
            new_media = media()
            
            infos = infos.text.splitlines()
            new_media.nom = infos[2]
            new_media.type = infos[3]
            new_media.categorie = infos[4]
            
            medias.append(new_media)
            media_index = media_index+1
        
        print("INDEX = " + str(media_index))
        media_index = 0
        
        for extra_infos in all_extra_infos:
            extra_infos = list(filter(None,extra_infos.text.splitlines()))
            #The number of tag is variable but it always follow the following pattern:
            #Tag_:Value  where _ = space
            tags = []
            values = []
            dict = {}
            for line in extra_infos:
                line = line.split(' :')
                if(len(line) < 2):
                    dict[previous_tag] = dict[previous_tag]+ " " + line[0]
                else:
                    tags.append(line[0])
                    all_tags.add(line[0])
                    values.append(line[1])
                    dict[line[0]] = line[1]
                    previous_tag = line[0]
            tag_value_dict.append(dict)
            medias[media_index].attr = tags
            medias[media_index].vals = values
            media_index = media_index + 1
        file.close()
        print("INDEX = " + str(media_index))
        with open("media_info.csv",'w',encoding='utf8',newline='') as mediafile:
            mediaCSV = csv.writer(mediafile,delimiter=',')
            header = ["index","name","type","category"]
            all_tags = list(all_tags)
            header = header + all_tags
            mediaCSV.writerow(header);
            
            for index in range(0,media_index):
                row = []
                row.append(str(index))
                row.append(medias[index].nom)
                row.append(medias[index].type)
                row.append(medias[index].categorie)           
                for tag in all_tags:
                    if tag in tag_value_dict[index]:
                        dict = tag_value_dict[index]
                        row.append(dict[tag])
                    else:
                        row.append("")
                
                mediaCSV.writerow(row)
