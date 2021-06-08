import scrapy
from currency.items import CurrencyItem
import datetime

class Currency(scrapy.Spider):
    name = "currency_spidey"
    
    def start_requests(self):
        urls = ["https://www.ashesh.com.np/forex/widget2.php?api=74426464455666vs"]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)



    def parse(self,response):
        items = CurrencyItem()
        
        lists = response.xpath('/html/body/div[contains(@class,"main")]//a')

        for link in lists:
            country_name = link.xpath("div[contains(@class,'country')]/div[contains(@class,'name')]/text()").get()
            selling_rate = link.xpath("div[contains(@class,'country')]/div[contains(@class,'rate_selling')]/text()").get()
            buying_rate = link.xpath("div[contains(@class,'country')]/div[contains(@class,'rate_buying')]/text()").get()
            date = datetime.datetime.now()
            date = date.strftime("%x")
            country_name = self.stripper(country_name)
            selling_rate = self.stripper(selling_rate)
            buying_rate = self.stripper(buying_rate)
            items['country'] = country_name
            items['buying_rate'] = float(buying_rate)
            items['selling_rate'] = float(selling_rate)
            items['date'] = date

            yield items
            
        
    def stripper(self,results):
        new = results.strip()
        return new
        # country_names = self.stripper(country_names)
        # buying_rates = self.stripper(buying_rates)
        # selling_rates = self.stripper(selling_rates)

        

        
        # item = CurrencyItem()

        # for country_name in country_names:
        #     item['country'] = country_name
             

        
            

    
        # a = dict(zip(country_names,zip(buying_rate,selling_rate)))

        # print(a)
        # for link in links:
        #     # print(link)
        #     # print("**************")
        #     country_name = link.xpath("/div[contains(@class,'country')]//div[contains(@class,'name')]/text()").extract()
        #     print(len(country_name))
