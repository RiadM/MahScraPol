# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import csv
from langdetect import detect_langs
from scrapy.linkextractors import LinkExtractor
import json
import codecs

class journalist:
    def __init__(self):
        fn = ""
        ln = "" 
        occ = ""
        jour = ""
        attr = []
        vals = []
        
class JournalistSpider(scrapy.Spider):
    name = 'journalist' #Name of the spider
    start_urls = ['https://membres.fpjq.org/index.php?vMenu=153&amp;vOptions=Membres'] #site we try to scrape
    def parse(self, response):
        request = scrapy.FormRequest.from_response(
            response,
            formname='recherche',
            formdata={'Prenom': '_'},
            callback=self.parse_recherche
            )
        print(request.body)
        yield request
        
    def parse_recherche(self,response):
        all_tags = set();
        journalists = []
        tag_value_dict = []
        
        soup = BeautifulSoup(response.body, "html.parser")
        all_regular_infos = soup.findAll("table",{'style':"width:90%; margin-top:7px;"})
        all_extra_infos = soup.findAll("div",{'class':"fiche"})
        file = open('test.html',"w",encoding='utf8')
        
        journalist_index = 0
        #Here we extract all the regular infor from the journalist
        for infos in all_regular_infos:
            new_journalist = journalist()
            
            infos = infos.text.splitlines()
            
            #Here we get the first and last name
            full_name = infos[2].split(', ')
            last_name = full_name[0]
            first_name = full_name[1]
            
            #Here we get the occupation and journal (if any)
            occupation = infos[3]
            journal = infos[4]
            
            #Here we save the data into the array
            new_journalist.fn = first_name
            new_journalist.ln = last_name
            new_journalist.occ = occupation
            new_journalist.jour = journal
            
            journalists.append(new_journalist)
            journalist_index = journalist_index+1

        print("INDEX = " + str(journalist_index))
        journalist_index = 0
        for extra_infos in all_extra_infos:
            extra_infos = list(filter(None,extra_infos.text.splitlines()))
            #The number of tag is variable but it always follow the following pattern:
            #Tag_:Value  where _ = space
            tags = []
            values = []
            dict = {}
            print(journalist_index)
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
             
            journalists[journalist_index].attr = tags
            journalists[journalist_index].vals = values
            journalist_index = journalist_index + 1
            #print(tags)
                
                
        print("INDEX = " + str(journalist_index))
            
        with open("journalist_info.csv",'w',encoding='utf8',newline='') as jourfile:
            jourCSV = csv.writer(jourfile,delimiter=',')
            header = ["index","firstname","lastname","occupation","journal"]
            all_tags = list(all_tags)
            header = header + all_tags
            jourCSV.writerow(header);
            
            for index in range(0,journalist_index):
                row = []
                row.append(str(index))
                row.append(journalists[index].fn)
                row.append(journalists[index].ln)
                row.append(journalists[index].occ)
                row.append(journalists[index].jour)                
                for tag in all_tags:
                    if tag in tag_value_dict[index]:
                        dict = tag_value_dict[index]
                        row.append(dict[tag])
                    else:
                        row.append("")
                
                jourCSV.writerow(row)
            

            
            
            
        file.close()
        #print(all_tags)