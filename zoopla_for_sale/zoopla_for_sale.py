# -*- coding: utf-8 -*-
import re
import scrapy
from datetime import datetime
from freeman.items import Zoopla


class ZooplaSpider(scrapy.Spider):
    name = "zoopla_for_sale"
    allowed_domains = ["zoopla.co.uk"]

    # rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="paginate"]',)), callback="parse_page", follow= True),)
    # start_urls = ['https://www.zoopla.co.uk/for-sale/houses/e15/?q=e15&radius=0&property_sub_type=&beds_min=&beds_max=&price_max=&price_min=&page_size=100']
    # def __init__(self, property_type='houses', location='e14,e15', radius=0,property_sub_type='',beds_min='',beds_max='',price_max='',price_min='',page_size=25, **kwargs):
    def __init__(
        self,
        property_type="houses",
        location="e10,e11,e12,e13,e14,e15,e16,e17,e18,e20",
        radius=0,
        property_sub_type="",
        beds_min="",
        beds_max="",
        price_max="",
        price_min="",
        page_size=25,
        **kwargs
    ):
        urls = []

        if "," in location:
            location_list = location.split(",")
            for new_location in location_list:
                new_location = new_location.lower()
                url = "https://www.zoopla.co.uk/for-sale/{0}/{1}/?q={2}&radius={3}&property_sub_type={4}&beds_min{5}&beds_max={6}&price_max={7}&price_min={8}&page_size={9}".format(
                    property_type,
                    new_location,
                    new_location,
                    radius,
                    property_sub_type,
                    beds_min,
                    beds_max,
                    price_max,
                    price_min,
                    page_size,
                )
                urls.append(url)
        else:
            location = location.lower()
            url = "https://www.zoopla.co.uk/for-sale/{0}/{1}/?q={2}&radius={3}&property_sub_type={4}&beds_min{5}&beds_max={6}&price_max={7}&price_min={8}&page_size={9}".format(
                property_type,
                location,
                location,
                radius,
                property_sub_type,
                beds_min,
                beds_max,
                price_max,
                price_min,
                page_size,
            )
            urls.append(url)
            # print urls

        # Rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="paginate"]/a[contains(text(),"Next")',)), callback="parse", follow= True),)

        self.start_urls = urls
        super(ZooplaSpider, self).__init__(**kwargs)

    def parse(self, response):
        houses = response.xpath("//div[contains(@id, 'content')]/ul/li")
        try:
            next_page = response.xpath("//div[contains(@class, 'paginate')]/a/text()")[
                -1
            ].extract()
        except Exception as e:
            next_page = ""

        for house in houses:
            item = Zoopla()
            prices = house.xpath("div/div/a/text()").extract()
            description = house.xpath("div/div/a/@href").extract()
            bedrooms = house.xpath(
                "div/div/h3/span[contains(@class, 'num-beds')]/text()"
            ).extract()
            summaries = house.xpath(
                "//div[contains(@class, 'listing-results-right clearfix')]/p/text()"
            ).extract()
            addresses = house.xpath(
                "div/div/span/a[contains(@class, 'listing-results-address')]/text()"
            ).extract()
            bathrooms = house.xpath(
                "div/div/h3/span[contains(@class, 'num-baths')]/text()"
            ).extract()
            reception_rooms = house.xpath(
                "div/div/h3/span[contains(@class, 'num-reception')]/text()"
            ).extract()
            agent_phone = house.xpath(
                "div/div/div/p/span[contains(@class, 'agent_phone')]/a/span/text()"
            ).extract()
            station_distances = house.xpath(
                "div/div/div[contains(@class, 'nearby_stations_schools')]/ul/li/text()"
            ).extract()
            agent = house.xpath(
                "div/div/div/p[contains(@class, 'listing-results-marketed')]/span/text()"
            ).extract()
            # latitude=house.xpath("div/div/div[contains(@itemprop, 'geo')]/meta[contains(@itemprop, 'latitude')]/@content").extract()
            # longitude=house.xpath("div/div/div[contains(@itemprop, 'geo')]/meta[contains(@itemprop, 'longitude')]/@content").extract()
            stations = house.xpath(
                "div/div/div[contains(@class, 'nearby_stations_schools')]/ul/li/span[contains(@class, 'nearby_stations_schools_name')]/text()"
            ).extract()

            formatted_beds = self.parse_string(bedrooms)
            formatted_price = self.parse_string(prices)
            formatted_agent = self.parse_string(agent)
            formatted_summary = self.parse_string(summaries)
            formatted_address = self.parse_string(addresses)
            # formatted_latitude=self.parse_string(latitude)
            # formatted_longitude=self.parse_string(longitude)
            formatted_bathrooms = self.parse_string(bathrooms)
            formatted_stations = self.parse_list_string(stations)
            formatted_agent_phone = self.parse_string(agent_phone)
            formatted_description = self.parse_string(description)
            formatted_reception_rooms = self.parse_string(reception_rooms)
            formatted_station_distance = self.parse_list_with_strip_string(
                station_distances
            )

            formatted_beds = int(formatted_beds) if formatted_beds else 0
            formatted_bathrooms = int(formatted_bathrooms) if formatted_bathrooms else 1
            try:
                formatted_price = (
                    int(re.sub("\D", "", formatted_price)) if formatted_price else None
                )
            except Exception as e:
                formatted_price = None
            # formatted_latitude=Decimal(formatted_latitude) if formatted_latitude else 0
            # formatted_longitude=Decimal(formatted_longitude) if formatted_longitude else 0
            formatted_reception_rooms = (
                int(formatted_reception_rooms) if formatted_reception_rooms else 0
            )

            item["asking_price"] = formatted_price
            item["agent"] = formatted_agent
            item["address"] = formatted_address
            item["summary"] = formatted_summary
            item["stations"] = formatted_stations
            # item['latitude']=formatted_latitude
            # item['longitude']=formatted_longitude
            item["search_result_url"] = response.url
            item["agent_number"] = formatted_agent_phone
            item["station_distances"] = formatted_station_distance
            item["bedrooms"] = formatted_beds
            item["bathrooms"] = formatted_bathrooms
            item["reception_rooms"] = formatted_reception_rooms

            if formatted_description:
                item["listing_url"] = "https://www.zoopla.co.uk" + formatted_description
                formatted_url = "https://www.zoopla.co.uk" + formatted_description
                request = scrapy.Request(url=formatted_url, callback=self.parse_url)
                request.meta["item"] = item

                yield request

        try:
            if next_page.strip() == "Next":
                next_url = response.xpath(
                    "//div[contains(@class, 'paginate')]/a/@href"
                )[-1].extract()
                next_url = next_url.strip()
                formatted_url = "https://www.zoopla.co.uk" + next_url
                next_url = response.urljoin(next_url)
                # print("next_url", next_url)
                yield scrapy.Request(next_url, callback=self.parse)
        except Exception as e:
            print("No next page")

    def parse_string(self, items):
        for item in items:
            return item.strip()

    def parse_list_string(self, items):
        formatted_list = []
        for item in items:
            formatted_item = item.strip()
            if formatted_item:
                formatted_list.append(formatted_item)
        return formatted_list

    def parse_list_with_strip_string(self, items):
        formatted_list = []
        for item in items:
            formatted_item = item.strip()
            if formatted_item:
                formatted_list.append(formatted_item[1:-1])
        return formatted_list

    def concate_string(self, item_details):
        formatted_item_details = ""

        for item_detail in item_details:
            formatted_item_detail = item_detail.strip()
            if formatted_item_detail:
                formatted_item_details = formatted_item_details + formatted_item_detail

        return formatted_item_details

    def date_parser(self, date):
        return re.sub(r"(\d)(st|nd|rd|th)", r"\1", date)

    def parse_url(self, response):
        formatted_item_details = ""
        formatted_postcode = ""
        formatted_agency_postcode = ""
        scripts = response.xpath("//script").extract()
        item = response.meta["item"]

        listing_history = response.xpath(
            '//section[contains(@class, "dp-price-history-block")]'
        )
        updated_price_list = response.xpath(
            '//div[contains(@class, "sidebar sbt")]/div[contains(@class, "top")]/ul/li'
        )

        # listing_history=response.xpath('//h4[contains(@text, "Listing history")]/ancestor::div[contains(@class, "sidebar sbt")]').extract()
        # listing_history=response.xpath('//div[@class="sidebar sbt" and contains(.//h4, "Listing history")]')
        # first_marketed_div = response.xpath('//div[contains(@id, "listings-agent")]/div')[3]
        # first_marketed_p=first_marketed_div.xpath('p/text()').extract()[1]
        # postcode = response.xpath('//a[contains(@class, "tabs-right-link")]/@href').extract()[0]
        description_details = response.xpath(
            '//div[contains(@class, "dp-description__text")]//text()'
        ).extract()
        # local_authorities = response.xpath('//div[contains(@id, "content")]/div/div/div[contains(@id, "tab-local")]/div/ul/li/a/span/text()').extract()
        local_authorities = response.xpath(
            '//h2[contains(text(), "Local info for")]/text()'
        ).extract()

        tenure = ""
        property_type = ""
        last_listed_date = ""
        first_listed_date = ""
        latitude = None
        longitude = None

        last_listed_price = None
        first_listed_price = None

        # If the postal code is not found, we will try to search in scripts tag below
        try:
            postcode = response.xpath(
                '//a[contains(@class, "dp-broadband-speed__link")]/@href'
            ).extract()[0]
            postcode = postcode.split("postcode=")[1].split("&")[0]
            formatted_postcode = postcode.strip()
        except Exception as e:
            formatted_postcode = ""

        if len(listing_history):
            price_histories = listing_history.xpath(
                'div[contains(@class, "dp-price-history__item")]'
            )
            for price_history in price_histories:
                price_history_details = price_history.xpath(
                    'span[contains(@class, "dp-price-history__item-detail")]/text()'
                ).extract()[0]
                if "first listed" in price_history_details.lower():
                    first_date = price_history.xpath(
                        'span[contains(@class, "dp-price-history__item-date")]/text()'
                    ).extract()[0]
                    first_price = price_history.xpath(
                        'span[contains(@class, "dp-price-history__item-price")]/text()'
                    ).extract()[0]
                    first_listed_price = (
                        int(re.sub("\D", "", first_price)) if first_price else None
                    )
                    first_listed_date = (
                        datetime.strptime(self.date_parser(first_date), "%d %b %Y")
                        if first_date
                        else ""
                    )

                if "last sold" in price_history_details.lower():
                    last_date = price_history.xpath(
                        'span[contains(@class, "dp-price-history__item-date")]/text()'
                    ).extract()[0]
                    last_price = price_history.xpath(
                        'span[contains(@class, "dp-price-history__item-price")]/text()'
                    ).extract()[0]
                    last_listed_price = (
                        int(re.sub("\D", "", last_price)) if last_price else None
                    )
                    last_listed_date = (
                        datetime.strptime(self.date_parser(last_date), "%d %b %Y")
                        if last_date
                        else ""
                    )

        for script in scripts:
            if "ZPG.trackData.taxonomy" in script:
                if "property_type" in script:
                    property_type = script.split("property_type:")[-1].split(",")[0]
                if "tenure" in script:
                    tenure = script.split("tenure:")[-1].split(",")[0]
                if "outcode" in script:
                    outcode = (
                        script.split("outcode:")[-1]
                        .split(",")[0]
                        .replace('"', "")
                        .strip()
                    )
                    incode = (
                        script.split("incode:")[-1]
                        .split(",")[0]
                        .replace('"', "")
                        .strip()
                    )
                    formatted_postcode = str(outcode) + " " + str(incode)

            if "postalCode" in script:
                agency_postcode = script.split('"postalCode":')[-1].split("}")[0]
                formatted_agency_postcode = (
                    agency_postcode.strip('"').strip() if agency_postcode else ""
                )
                formatted_agency_postcode = (
                    formatted_agency_postcode.strip('"')
                    if formatted_agency_postcode
                    else ""
                )

            if ("ZPG.mapData") in script:
                mapData = script.split("ZPG.mapData =")[-1].split('"pin"')[0]
                latitude = mapData.split('"latitude":')[-1].split(",")[0]
                longitude = mapData.split('"longitude":')[-1].split("}")[0]

        try:
            if not formatted_agency_postcode:
                agency_postcode = response.xpath(
                    '//meta[contains(@property, "og:postal-code")]/@content'
                ).extract()[0]
                formatted_agency_postcode = agency_postcode.strip()
        except Exception as e:
            print("Post code not found")

        property_type = property_type.strip().replace('"', "") if property_type else ""
        property_type = re.sub(r"[_|-]", r" ", property_type)
        updated_price_rate_list = updated_price_list.xpath("strong/text()").extract()
        updated_price_date_list = updated_price_list.xpath(
            'span[contains(@class, "date")]/text()'
        ).extract()

        if updated_price_date_list:
            updated_price_rate = updated_price_rate_list[-1].strip()
            updated_price_date_list = (
                updated_price_date_list[-1].split("on:")[1].strip()
            )
            price_last_updated = (
                datetime.strptime(self.date_parser(updated_price_date_list), "%d %b %Y")
                if updated_price_date_list
                else ""
            )
        else:
            price_last_updated = 0
            updated_price_rate = 0

        formatted_description = self.concate_string(description_details)
        formatted_local_authority = self.concate_string(local_authorities)
        # try:
        #     formatted_first_marketed=first_marketed_p.replace('\n', '')
        # except Exception as e:
        #     formatted_first_marketed=''

        item["last_sold_date"] = last_listed_date
        item["price_adjusted"] = updated_price_rate
        item["last_sold_price"] = last_listed_price
        item["first_listed_date"] = first_listed_date
        item["description"] = formatted_description
        item["postcode"] = formatted_postcode
        if latitude:
            item["latitude"] = latitude.strip()
        if longitude:
            item["longitude"] = longitude.strip()
        item["asking_price_updated"] = price_last_updated
        item["first_listed_asking_price"] = first_listed_price
        item["property_type"] = property_type.title()
        tenure = tenure.strip('"').strip() if tenure else ""
        item["tenure"] = tenure.strip('"').strip() if tenure else ""
        # item['postcode']=formatted_postcode.split('postcode=')[1] if formatted_postcode else ''
        item["agency_postcode"] = formatted_agency_postcode
        # try:
        #     formatted_first_marketed=formatted_first_marketed.split('on')[1].strip() if formatted_first_marketed else ''
        # except Exception as e:
        #     formatted_first_marketed=''
        item["local_authority"] = (
            formatted_local_authority.split("for")[1].strip()
            if formatted_local_authority
            else ""
        )
        # item['first_marketed']=datetime.strptime(self.date_parser(formatted_first_marketed), '%d %b %Y') if formatted_first_marketed else ''

        yield item
