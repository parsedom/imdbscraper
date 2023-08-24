import scrapy


class MoviescraperSpider(scrapy.Spider):
    name = "moviescraper"
    start_urls = ["https://www.imdb.com/search/title/?genres=Action&explore=title_type%2Cgenres"]

    def parse(self, response):
        headers = {
    "authority": "www.imdb.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US,en;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Brave\";v=\"116\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "sec-gpc": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
        links = response.xpath('//div[@class = "lister-item-content"]/h3[@class = "lister-item-header"]//a/@href').getall()
        # breakpoint()
        for link in links:
            yield scrapy.Request(
                url= 'https://imdb.com' + link,
                callback=self.parse_detail,
                headers=headers
            )
        next_btn = response.xpath('//a[@class = "lister-page-next next-page"]/@href').get()
        if next_btn:
            yield scrapy.Request(
                url = 'https://imdb.com' + next_btn,
                callback= self.parse
            )
        
    def parse_detail(self,response):
        Title = response.xpath('//h1[@data-testid = "hero__pageTitle"]/span/text()').get()
        rating_score = response.xpath('//div[@data-testid= "hero-rating-bar__aggregate-rating__score"]/span/text()').get()
        summary = response.xpath('//span[@data-testid="plot-xl"]/text()').get()
        cast_details = response.xpath('//section[@data-testid= "title-cast"]')
        Director = cast_details.xpath('//li[@role="presentation"]/span[text() ="Director"]/following-sibling::div//li[@role= "presentation"]/a/text()').get()
        Writers = cast_details.xpath('//li[@role="presentation"]/*[text() ="Writer"]/following-sibling::div//li[@role= "presentation"]/a/text()').getall()
        Stars = cast_details.xpath('//li[@role="presentation"]/*[text() ="Stars"]/following-sibling::div//li[@role= "presentation"]/a/text()').getall()
        Writer_newlist = []
        for i in Writers:
            if i not in Writer_newlist:
                Writer_newlist.append(i)

        Stars_newlist = []
        for i in Writers:
            if i not in Stars_newlist:
                Stars_newlist.append(i)       

        yield {
            'Title' : Title,
            'Rating' : rating_score ,
            'summary' : summary ,
            'Director' : Director,
            'Writer' : Writer_newlist , 
            'Stars' : Stars_newlist
        }