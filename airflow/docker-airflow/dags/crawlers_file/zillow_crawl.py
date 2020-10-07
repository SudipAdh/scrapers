import requests
from bs4 import BeautifulSoup
import csv
class ZillowCrawler:

    def __init__(self,zip_codes):
        self.result = []
        self.zip_codes = zip_codes
        for each in self.zip_codes:
            self.each = each
            self.url = "https://www.zillow.com/homes/"+str(each)+"_rb/"
        
            self.header = {
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
            }


            self.crawl()

            self.write_to_csv()
    def crawl(self):
        try:
            response = requests.get(self.url, headers=self.header)
            
            soup = BeautifulSoup(response.content, 'lxml')

            print(soup.prettify())
            warning = soup.find('div', class_='SearchPageListContainer__StyledPaddedSearchInfoMessage-vcxez1-0 hKxLTs')
            if warning:
                print('No any matched found in the area.....')
            else:
            
        
                result_count = soup.select('span.result-count')[0].text.split()[0]
                print("Found {} homes for sales in area {}".format(result_count, self.each))
                articles = soup.select('div.result-list-container')[0].find("ul", class_="photo-cards photo-cards_wow photo-cards_short").find_all("article")
            
                self.data_extractor(articles, result_count, soup)

        except Exception as error:
            print(error)
            print(self.url)
            pass

    def data_extractor(self, articles, result_count, soup):
        for each in articles:
            price = each.find('div', class_="list-card-price").text.replace("$", "").replace(",", "").replace("+", "")
            if price.startswith("E"):
                
                price = price.replace("Est. ", "") 
            else:
                price
            address = each.find('address', class_="list-card-addr").text
            
            prop_type = each.find('div', class_="list-card-type").text
            
            details_ul = each.find('ul', class_="list-card-details")

            url = each.find('div', class_="list-card-info").find("a").get('href')
           
            try:
                li_items = details_ul.find_all('li')
                bds = li_items[0].text
                ba = li_items[1].text
                area = li_items[2].text
                

            except Exception:
                bds = None
                ba = None
                area = None
            
            if bds:
               bds = bds.split()[0]
            elif bds == "--":
                
                bds = None
            else:
                
                pass 
            if ba:
               ba = ba.split()[0]
            elif ba == "--":
                ba = None
            else:
                pass 

            if area:
               area = area.split()[0].replace(",", "")
            else:
                pass 

            bds = self.intmaker(bds)
            ba = self.intmaker(ba)
            area = self.intmaker(area)      
            zip_code = self.each
            data = {
                "location": address,
                "price": price,
                "type": prop_type,
                "bds": bds,
                "ba": ba,
                "area": area,
                "zip_code": zip_code,
                "url": url,
                "total_found": result_count

            }
            self.result.append(data)
        try:
            next_page_li = soup.find("ul", class_="StyledPaginationList-sc-2vwigm-1 jzUAIw")
            page_info = next_page_li.find_all("li", class_="PaginationNumberItem-bnmlxt-0 kdxFbt")
            current_page = [li.text for li in page_info if "current page" in li.find("a").get("title")]
            next_page_link = next_page_li.find_all("li")
            next_page_link = [li.find("a")for li in next_page_link if "Next page" in li.find("a").get("title")]
            # next_page_a = [li.find("a") for li in next_page_link if "Next page" in li.find("a").get("title")]
            # print(next_page_a)
            print("On page {}.............".format(current_page[0]))
            if next_page_link[0].has_attr('disabled'):
                print("Finished Crawling For {}".format(self.each))
            else:
                self.url = "https://www.zillow.com"+next_page_link[0].get("href")
                self.crawl()
        except Exception:
            pass
        
            
        
    def intmaker(self, data):
        try:
            return int(data)
        except Exception:
            return None





    def write_to_csv(self):
        with open("zillow_property.csv", "w") as file:
            dict_writer = csv.DictWriter(file, fieldnames=['location', 'price', 'type', 'bds', 'ba', 'area', 'zip_code', 'url', 'total_found'])
            dict_writer.writeheader()
            dict_writer.writerows(self.result)


# file = open('../zip_codes.csv', 'r')
# zip_codes = [line.strip() for line in file.readlines()]
# crawl = ZillowCrawler(zip_codes)