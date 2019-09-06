import scrapy

class Report(scrapy.Spider):
    name = "report"
    allowed_domains = ['ipaidabribe.com']
    start_urls = [
        'http://www.ipaidabribe.com/reports/paid?page=',
    ]

    npages = 100
    for i in range(20, npages + 10):
        start_urls.append("http://www.ipaidabribe.com/reports/paid?page=" + str(i) + "")

    def parse(self, response):
        report = response.css('.ref-module-paid-bribe')
        title = report.css(".heading-3>a::text").extract(),
        amount = report.css(".paid-amount>span::text").extract(),
        name_of_dept = report.css(".department.clearfix>li>a::text").extract(),
        transaction_detail = report.css(".body-copy-lg::text").extract(),
        views = report.css(".views::text").extract(),
        city = report.css(".key>a::text").extract(),
        date = report.css(".key>span::text").extract(),
        for p in range(len(title)):
            yield {
                'title' : title[p],
                'amount' : amount[p],
                'name_of_dept' : name_of_dept[p],
                'transaction_detail' : transaction_detail[p],
                'views' : views[p],
                'city' : city[p],
                'date' : date[p],
            }

        next_page_url = response.css("li.active > a::attr(href)").extract_first()
        if next_page_url:
            yield scrapy.Request(
                response.urljoin(next_page_url),
                callback=self.parse
            )
