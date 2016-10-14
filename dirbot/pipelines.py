from scrapy.exceptions import DropItem


class FilterWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""

    # put all words in lowercase
    words_to_filter = ['politics', 'religion','\u671f\u8d27']

    def process_item(self, item, spider):
        for word in self.words_to_filter:
            if word in unicode(item['name']).lower():
                raise DropItem("Contains forbidden word: %s" % word)
        else:
            return item