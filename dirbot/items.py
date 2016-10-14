from scrapy.item import Item, Field


class Website(Item):

    loupan = Field()
    location = Field()
    district = Field()
    housetype = Field()
    area = Field()
    decoration = Field()
    onsold = Field()
    live = Field()
    avgprice = Field()
    
class SecondHouse(Item):

    dataid = Field()
    city = Field()
    district = Field()
    title = Field()
    zonename = Field()
    housetype = Field()
    square = Field()
    direction = Field()
    remark = Field()
    subway = Field()
    taxfree = Field()
    education = Field()
    totalprice = Field()
    perprice = Field()
    review = Field()

