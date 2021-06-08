import scrapy
from My_Republica.items import MyRepublicaItem


class MyRepublica(scrapy.Spider):
    name = "republica_spidey"

    
    def start_requests(self):
        urls = [
                "https://myrepublica.nagariknetwork.com/"
            ]
        for url in urls:
            yield scrapy.Request(url= url,callback=self.parse)

    def parse(self,response):
        print(response.url)
        print(response.xpath("//title/text()").extract())
        
        
        # ignore = ["https://myrepublica.nagariknetwork.com/"]
        category_list = response.xpath("/html/body//nav//ul//li[contains(@class,'')]//a/@href").extract()

        for list in category_list:
            
            if list.startswith("/category"):
                list = list.replace("/","https://myrepublica.nagariknetwork.com/",1)
                yield scrapy.Request(url=list,callback=self.parse_news)
            else:
                continue
            

    def parse_news(self,response):
        
        
        upto_news_href = response.xpath("/html/body//section//div[contains(@class,'main-heading')]/a")   
        
        

        for href in upto_news_href:
            href = href.xpath("@href").extract()
            if href[0].startswith("/"):
                href[0] = href[0].replace("/","https://myrepublica.nagariknetwork.com/",1)
                
                yield scrapy.Request(url=href[0],callback=self.content_scraper)
            
            else:
                continue
    
    
    def content_scraper(self,response):
        link = response.url 
        if link.startswith("https://myrepublica.nagariknetwork.com/mycity"):
            news_title = response.xpath("/html/body/main//h2[contains(@class,'article__header__title')]/text()").get()
            published_date = response.xpath('/html/body/main/section//span[contains(@class,"date")]//text()').extract()
            actual_date = published_date[1].strip()
            actual_date = self.replacer(actual_date)
            source = response.xpath("/html/body/main/section//span[contains(@class,'date')]//a/text()").get()
            description = response.xpath("/html/body/main//section//div[contains(@class,'flex__item article__body__description')]//p//text()").extract()
            description = " ".join([each for each in description])
            description = self.replacer(description)
            urls = response.url
        else:
            news_title =response.xpath("/html/body//div[contains(@class,'main-heading')]//h2/text()").get()
            news_title = news_title.strip()
            published_date = response.xpath("/html/body//div[contains(@class,'headline-time')]//p//text()").extract() 
            actual_date = published_date[1].strip()
            actual_date = self.replacer(actual_date)
            source = response.xpath("/html/body//div[contains(@class,'headline-time pull-left')]//a/text()").get()
            description = response.xpath("/html/body//section//div[contains(@id,'newsContent')]//p//text()").extract()
            description = " ".join([each for each in description])
            description = self.replacer(description)
            
            urls = response.url

        items = MyRepublicaItem()

        items["title"] = news_title
        items["published_date"] = actual_date
        items["source"] = source
        items["description"] = description
        items["url"] = urls  

        yield items
        
        
    def replacer(self,strings):
        #new = strings.replace("\xa0","")(can't deploy to scrapinghub due to this error)
        new = strings.replace("\r\n","")
        new = new.replace("\n                                                                                            By:","")
        return new


            

    





