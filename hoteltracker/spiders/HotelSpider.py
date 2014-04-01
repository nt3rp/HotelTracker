from datetime import datetime
from time import strptime, strftime
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.spider import Spider
from urlparse import urlparse
from urllib import urlencode
from hoteltracker import settings
from hoteltracker.items import Hotel


class HotelSpider(Spider):
    url_template = None
    date_format = None
    use_query_params = False

    # TODO: Display Name, Shortname, etc.
    def __init__(self, check_in=None, check_out=None, location_code=None, group_code=''):
        assert location_code is not None, 'No location provided'
        assert check_in is not None, 'No check-in date provided'
        assert check_out is not None, 'No check-out date provided'
        assert self.url_template is not None, 'No URL template provided'
        assert self.date_format is not None, 'No date format provided'

        self.check_in = strftime(
            self.date_format,
            strptime(check_in, settings.DATE_FORMAT)
        )
        self.check_out = strftime(
            self.date_format,
            strptime(check_out, settings.DATE_FORMAT)
        )

        self.group_code = group_code
        self.location_code = location_code

        url = self.url_template.format(location_code)
        if self.use_query_params:
            url = '{0}?{1}'.format(url, urlencode(self.populate_params()))

        self.start_urls = [url]

    def parse(self, response):
        if not self.use_query_params:
            return self.submit_form(response)

        return self.get_results(response)

    def submit_form(self, response):
        sel = Selector(response)

        urls = sel.css(self.form_css)

        if not urls:
            # Logging: Error
            pass

        url = urls[0].extract()

        # Need to append base URL
        if not url.startswith('http'):
            host = '{uri.scheme}://{uri.netloc}'.format(
                uri=urlparse(response.url)
            )

            slash = '/' if not url.startswith('/') else ''

            url = '{host}{slash}{path}'.format(
                host=host,
                path=url,
                slash=slash
            )

        return [FormRequest(
            url=url,
            formdata=self.populate_params(),
            callback=self.get_results
        )]

    def create_item(self, name=None, available=False):
        if not name:
            name = self.name

        item = Hotel()
        item['name'] = name
        item['available'] = available
        item['last_updated'] = datetime.now()

        return item


    def get_results(self, response):
        if self.has_search_results(response):
            return self.parse_search_results(response)

        # TODO: Other conditions?

        return self.parse_unknown(response)

    def populate_params(self):
        raise NotImplementedError('No method defined for \'populate_params\'')

    def has_search_results(self, response):
        raise NotImplementedError('No method defined for \'is_search_results\'')

    def parse_search_results(self, response):
        raise NotImplementedError('No method defined for \'parse_search_results\'')

    def parse_unknown(self, response):
        raise NotImplementedError('No method defined for \'parse_unknown\'')