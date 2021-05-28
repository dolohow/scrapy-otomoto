import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Compose
from urllib.parse import urlparse
from otomoto.items import OtomotoItem

def filter_out_array(x):
    x = x.strip()
    return None if x == '' else x

def remove_spaces(x):
    return x.replace(' ', '')

def convert_to_integer(x):
    price = x.replace(',', '.')
    return int(price)

def convert_vin(x):
    if "?vin=" in x:
        vin = (urlparse(x).query.split('vin=', 1)[1]).split('&', 1)[0]
        if len(vin) != 17:
            vin = 'null'
    else:
        vin = 'null'
    return vin

class OtomotoCarLoader(ItemLoader):
    default_output_processor = TakeFirst()
    vin_in = MapCompose(convert_vin)
    features_out = MapCompose(filter_out_array)
    price_out = Compose(TakeFirst(), remove_spaces, convert_to_integer)


class OtomotoSpider(scrapy.Spider):

    name = 'otomoto'
    
    def __init__(self, *args, **kwargs): 
        super(OtomotoSpider, self).__init__(*args, **kwargs) 
        self.port = None
        self.start_urls = [kwargs.get('start_url')] 

    def parse(self, response):
        for car_page in response.css('.offer-title__link::attr(href)'):
            yield response.follow(car_page, self.parse_car_page)

        for next_page in response.css('.next.abs a::attr(href)'):
            yield response.follow(next_page, self.parse)

    def parse_car_page(self, response):
        property_list_map = {
            'Marka pojazdu': 'brand',
            'Model pojazdu': 'model',
            'Rok produkcji': 'year',
            'Wersja': 'version',
            'Przebieg': 'mileage',
            'Pojemność skokowa': 'capacity',
            'Moc': 'horse_power',
            'Rodzaj paliwa': 'fuel_type',
            'Skrzynia biegów': 'transmission',
            'Typ': 'type',
            'Liczba drzwi': 'number_of_doors',
            'Kraj pochodzenia': 'origin_country',
            'Kolor': 'color',
            'Pierwszy właściciel': 'first_owner',
            'Bezwypadkowy': 'no_accidents',
            'Serwisowany w ASO': 'aso',
            'Stan': 'condition',
            'Oferta od': 'seller',
            'Napęd': 'drivetrain',
            'Możliwość finansowania': 'financing',
            'Faktura VAT': 'invoice',
            'Numer rejestracyjny pojazdu': 'plates',
            'Pierwsza rejestracja': 'registration_date',
        }
        loader = OtomotoCarLoader(OtomotoItem(), response=response)

        for params in response.css('.offer-params__item'):
            property_name = params.css('.offer-params__label::text').extract_first().strip()
            if property_name in property_list_map:
                css = params.css('.offer-params__value::text').extract_first().strip()
                if css == '':
                    css = params.css('a::text').extract_first().strip()
                loader.add_value(property_list_map[property_name], css)

        loader.add_css('price', '.offer-price__number::text')
        loader.add_css('price_currency', '.offer-price__currency::text')
        loader.add_xpath('ad_id', '//span[@id="ad_id"]/text()')
        loader.add_xpath('published_at', '//div[@class="offer-meta"]/span/span/text()')
        loader.add_value('vin', response.css('[class=carfax-wrapper] div::attr(data-props)').get())
        loader.add_css('features', '.offer-features__item::text')
        loader.add_value('url', response.url)

        yield loader.load_item()
