import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Compose

from otomoto.items import OtomotoItem


def filter_out_array(x):
    x = x.strip()
    return None if x == '' else x


def remove_spaces(x):
    return x.replace(' ', '')


def convert_to_integer(x):
    y = x.split(',', 1)[0]
    return int(y)

def convert_vin(x):
    if "?vin=" in x:
        y = (x.split('?vin=', 1)[1]).split('#utm', 1)[0].split('&', 1)[0]
        if len(y) != 17:
            y = 'null'
    else:
        y = 'null'
    return y

class OtomotoCarLoader(ItemLoader):
    default_output_processor = TakeFirst()

    features_out = MapCompose(filter_out_array)
    price_out = Compose(TakeFirst(), remove_spaces, convert_to_integer)
    vin_out = Compose(TakeFirst(), convert_vin)


class OtomotoSpider(scrapy.Spider):

    name = 'otomoto'
    start_urls = ['https://www.otomoto.pl/osobowe/']

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
        adid = response.xpath('//span[@id="ad_id"]/text()').extract_first()
        loader.add_value('ad_id', adid)
        date = response.xpath('//div[@class="offer-meta"]/span/span/text()').extract_first()
        loader.add_value('add_date', date)
        vinnumber = response.css('[class=carfax-wrapper] div::attr(data-props)').get()
        loader.add_value('vin', vinnumber)
        loader.add_css('features', '.offer-features__item::text')
        loader.add_value('url', response.url)

        yield loader.load_item()
