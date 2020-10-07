import requests
from bs4 import BeautifulSoup
import re
import csv
class Scraper:
    def __init__(self, tax_no):
        self.result = []
        header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
        }
        for each in tax_no:
            print(each)
            
            url = "http://tax.ocgov.com/tcwebm/web_tdn.asp?ReqTDN="+each
            response = requests.post(url, headers=header)
            print(response.url)

            soup = BeautifulSoup(response.content, 'lxml')
            try:
                self.extractor(each, soup)
            except Exception:
                continue
    def extractor(self, each, soup):
            data = {}
            all_data = soup.findAll("div", {"class":"rTableCellSeven"})
            for each in all_data:
                    a = each.find("a")
                    if a:
                       
                        data["APN"] = a.text.strip().split(".")[0]
                    else:
                        continue
            ned = soup.findAll('div', {"class":"contentbold2"})
            
            year = soup.findAll("div", {"class":"contentbold2"})[5]
            location = soup.findAll("div", {"class":"contentbold2"})[8].get_text()
            earliest_delinquent_year = year.get_text()
            data["tax_default"] = each
            data["earliest_delinquent_year"] = earliest_delinquent_year
            data["TDN Parcels"] = all_data[7].get_text().strip()
            data["Apn Location"] = location
            data["RollYear"] = all_data[8].get_text().strip()
            data["Taxes"] = all_data[9].get_text().strip()
            data["BasicPenalties"] = all_data[10].get_text().strip()
            data["Cost"] = all_data[11].get_text().strip()
            data["Add'lPenalties"] = all_data[12].get_text().strip()
            data["Total"] = all_data[13].get_text().strip()
            data["location"] = location
            if len(all_data) == 24:
                data["(Less) Amount Paid"] = all_data[-3].get_text().strip()
            elif len(all_data) == 25:
                data["(Less) Amount Paid"] = all_data[-4].get_text().strip()
            data[all_data[14].get_text().strip()] = all_data[15].get_text().strip()
            data[all_data[16].get_text().strip()] = all_data[17].get_text().strip()
            data[all_data[18].get_text().strip()] = all_data[19].get_text().strip()
            #data[all_data[20].get_text().strip()] = all_data[21].get_text().strip()
            data[all_data[22].get_text().strip()] = all_data[23].get_text().strip()
            #try:
                #last_data = soup.findAll("div", {"class":"contentbold2"})[24]
                #data[last_data.get_text().strip()] = all_data[24].get_text().strip()
            #except:
                #pass
            print(data)
            self.result.append(data)

    def save_to_csv(self):

        keys = self.result[0].keys()
        with open('tcwebm.csv', 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.result)
            



sc = Scraper(['19000001','19000002', '19000005'])
sc.save_to_csv()