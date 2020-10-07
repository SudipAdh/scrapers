import requests
from bs4 import BeautifulSoup
import time
import os
class Scraper:
    
    def __init__(self):
        
        base_url = "https://www.gov.uk/topic"
        links = self.requester_and_soup_maker(base_url)
        for each in links:
            sub_links = self.requester_and_soup_maker(each)
            for each in sub_links:
                sub_sub_links = self.requester_and_soup_maker(each)
                for each in sub_sub_links:
                    main_soup = self.soup_maker(each)
                    self.data_crawler(main_soup)


    def data_crawler(self, main_soup):
        # print("in data_crawler")
        self.attachment_downloader(main_soup)
        links = main_soup.find_all("a")
        for each in links:
            if "https://" in each['href']:
                link = each['href']
                
            else:
                link = "https://www.gov.uk" + each['href']
                
            
            self.check_pdf(link)
            
        
        
        
        

        

    def check_pdf(self,each):
        
        try:
            if ".pdf" in each or ".csv" in each or ".docx" in each or ".xls" in each or ".odt" in each or ".ods" in each:
                file_name = each.split("/")[-1]
                if os.path.isfile("./files/"+str(file_name)):
                    print("Already Present")
                else:
                    response = self.downloading_response(each)
                    print("downloading............", each)
                    with open("./files/"+str(file_name), 'wb') as file:
                        file.write(response.content)
            elif "publications" in each:
                soup = self.soup_maker(each)
                self.attachment_downloader(soup)
            else:
                pass
        except Exception as error:
            print(error)
            print(each)
            
                

    def downloading_response(self, download_link):
        print("requesting.........")
        response = requests.get(download_link)
        return response

    def attachment_downloader(self,main_soup):
        attachment_class = main_soup.find_all("section", class_="attachment embedded")
        
        for each in attachment_class:
            try:
                download_link = each.find("h2", class_="title").find("a")['href']
                download_link = self.link_checker_and_formatter(download_link)
                file_name = download_link.split("/")[-1]
                
                if ".pdf" in file_name or ".csv" in file_name or ".docx" in file_name or ".xls" in file_name or ".odt" in file_name or ".ods" in file_name:
                    if os.path.isfile("./files/"+str(file_name)):
                        print("Already Present")
                    else:
                        response = self.downloading_response(download_link)
                        print("downloading##############", download_link)
                        with open("./files/"+str(file_name), 'wb') as file:
                            file.write(response.content)
                else:
                    continue
            except Exception:
                continue

    def requester_and_soup_maker(self,link):
        # print("in request&soup_maker")
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('li', class_='app-c-topic-list__item')
        links = ["https://www.gov.uk" + link.a['href'] for link in links]
        return links

    def soup_maker(self, links):
        # print("in soup_maker")
        
        response = requests.get(links)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def link_checker_and_formatter(self, link):
       
        if link.startswith("https://"):
            return link
        else:
            link= "https://www.gov.uk" + link
            return link

        

        

crawl = Scraper()
