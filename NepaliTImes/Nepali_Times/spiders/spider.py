import scrapy
from Nepali_Times.items import NepaliTimesItem
class Nepali_Times(scrapy.Spider):
    name = "nepali_times_spidey"

    def start_requests(self):
        urls = ["https://www.nepalitimes.com/"]

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self,response):
        news_category_links = response.xpath("/html/body//ul[contains(@class,'nav navbar-nav')]/li/a")
        ignore = ["https://www.nepalitimes.com/nt/editorial/",
                    "https://www.nepalitimes.com/",
                    "https://www.nepalitimes.com/nt/about-town/",
                    "http://archive.nepalitimes.com/issue_archive/list/2018",
                    "#"
                ]
        for link in news_category_links:
            href = link.xpath("@href").extract()
            if href[0] == ignore[0] or href[0] == ignore[1] or href[0] == ignore[2] or href[0] == ignore[3] or href[0] == ignore[4]:
                continue
            else:
                yield scrapy.Request(url=href[0],callback=self.news_list_scraper)
    
    def news_list_scraper(self,response):
    
        news_title_selector_check = response.xpath("/html/body//div[contains(@class,'col-xs-12 col-md-3 margin-bottom-50')]//h2/a").extract()
        if len(news_title_selector_check) != 0:
            news_title_selector = response.xpath("/html/body//div[contains(@class,'col-xs-12 col-md-3 margin-bottom-50')]//h2/a")
        elif len(news_title_selector_check) == 0:
            news_title_selector = response.xpath("/html/body//div[contains(@class,'col-xs-12 col-md-4 margin-bottom-50')]//header[contains(@class,'nt-video-header')]//a")

        
        for title_link in news_title_selector:
            href = title_link.xpath("@href").extract()
            
            
            yield scrapy.Request(url=href[0],callback=self.content_scraper)

    def content_scraper(self,response):
        
        news_title = response.xpath("/html/body//div[contains(@class,'about-page-detailing')]/h1/text()").get()
        date = response.xpath("/html/body//div[contains(@class,'about-page-detailing')]//span[contains(@class,'dates')]//text()").extract()
        actual_date = date[1]
        description = response.xpath("/html/body//div[contains(@class,'row')]//div[contains(@class,'elementor-text-editor elementor-clearfix')]//p//text()").extract()
        description = " ".join(description)

        item = NepaliTimesItem()

        item['title']=news_title
        item['date']=actual_date
        item['description']=description
        item['url']=response.url

        yield item