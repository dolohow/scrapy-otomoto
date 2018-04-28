import scrapy


class OtomotoItem(scrapy.Item):
    brand = scrapy.Field()
    model = scrapy.Field()
    year = scrapy.Field()
    mileage = scrapy.Field()
    capacity = scrapy.Field()
    horse_power = scrapy.Field()
    fuel_type = scrapy.Field()
    transmission = scrapy.Field()
    type = scrapy.Field()
    number_of_doors = scrapy.Field()
    color = scrapy.Field()
    first_owner = scrapy.Field()
    no_accidents = scrapy.Field()
    aso = scrapy.Field()
    condition = scrapy.Field()
    features = scrapy.Field()
    url = scrapy.Field()
