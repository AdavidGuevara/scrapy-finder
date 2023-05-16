import scrapy


class CompaniesSpider(scrapy.Spider):
    name = "companies"

    def start_requests(self):
        finABC = "abcdefghijklmnopqrstuvwxyzåäö"
        for letter in finABC:
            yield scrapy.Request(
                url=f"https://www.finder.fi/search?what={letter}&type=company&page=1",
                callback=self.parse,
                meta={"letter": letter, "page": 1},
            )

    def parse(self, response):
        letter = response.meta["letter"]
        page = response.meta["page"]

        companies = response.xpath("//div[contains(@class,'SearchResult--compact')]")
        for companie in companies:
            yield {
                "name": companie.xpath(
                    ".//div[@class='SearchResult__Name']/text()"
                ).get(),
                "info": [
                    info.strip()
                    for info in companie.xpath(
                        ".//div[@class='text-muted']/text()"
                    ).getall()
                ],
                "location": companie.xpath(
                    ".//a[@class='SearchResult__Link']/text()"
                ).get(),
                "url": companie.xpath(".//a[@class=' undefined']/@href").get(),
                "phone": companie.xpath(".//div[@class='PhoneNumber']/text()").get(),
            }

        if page == 1:
            pages = response.xpath(
                "//div[@class='SearchResultList__PageSelection SearchResultList__Navigation__Col']/ul/li/a/text()"
            ).getall()

        for page_number in range(2, int(pages[-1]) + 1):
            yield scrapy.Request(
                url=f"https://www.finder.fi/search?what={letter}&type=company&page={page_number}",
                callback=self.parse,
                meta={"letter": letter, "page": page},
            )
