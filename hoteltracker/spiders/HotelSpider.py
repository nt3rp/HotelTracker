from datetime import datetime
from time import strptime, strftime
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.spider import Spider
from urlparse import urlparse
from hoteltracker import settings
from hoteltracker.items import Hotel


class HotelSpider(Spider):
    url_template = None
    date_format = None

    # TODO: Display Name, Shortname, etc.
    def __init__(self, check_in=None, check_out=None, location_code=None, group_code=''):
        assert location_code is not None, 'No location provided'
        assert check_in is not None, 'No check-in date provided'
        assert check_out is not None, 'No check-out date provided'
        assert self.url_template is not None, 'No URL template provided'
        assert self.date_format is not None, 'No date format provided'

        self.start_urls = [self.url_template.format(location_code)]

        self.check_in = strftime(
            self.date_format,
            strptime(check_in, settings.DATE_FORMAT)
        )
        self.check_out = strftime(
            self.date_format,
            strptime(check_out, settings.DATE_FORMAT)
        )

        self.group_code = group_code

    def parse(self, response):
        sel = Selector(response)

        urls = sel.css(self.form_css)

        if not urls:
            # Logging: Error
            pass

        url = urls[0].extract()

        # Need to append base URL
        if url.startswith('/'):
            host = '{uri.scheme}://{uri.netloc}'.format(
                uri=urlparse(response.url)
            )
            url = '{host}{path}'.format(host=host, path=url)

        return [FormRequest(
            url=url,
            formdata=self.populate_search_form(),
            callback=self.after_post
        )]

    def create_item(self, name=None, available=False):
        if not name:
            name = self.name

        item = Hotel()
        item['name'] = name
        item['available'] = available
        item['last_updated'] = datetime.now()

        return item


    def after_post(self, response):
        if self.has_search_results(response):
            return self.parse_search_results(response)

        # TODO: Other conditions?

        return self.parse_unknown(response)

    def populate_search_form(self):
        raise NotImplementedError('No method defined for \'populate_search_form\'')

    def has_search_results(self, response):
        raise NotImplementedError('No method defined for \'is_search_results\'')

    def parse_search_results(self, response):
        raise NotImplementedError('No method defined for \'parse_search_results\'')

    def parse_unknown(self, response):
        raise NotImplementedError('No method defined for \'parse_unknown\'')