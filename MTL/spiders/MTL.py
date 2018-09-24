import scrapy

from MTL.items import MtlItem


class MtlSpider(scrapy.Spider):
    # 爬虫的名字
    name = 'mtl_img'
    # 允许的域名
    allowed_domains = ['www.meitulu.com']
    # 入口地址
    start_urls = ['https://www.meitulu.com/guochan/2.html']

    # 默认的解析方法
    def parse(self, response):
        # 主页上的图片入口地址
        img_links = response.xpath("//div[@class='boxs']/ul/li/a/@href").extract()
        for img_link in img_links:
            yield scrapy.Request(img_link, callback=self.parse_img)
        # 下一页
        next_links = response.xpath("//center/div[@id='pages']/a/@href").extract()
        for next_suffix_link in next_links:
            next = "https://www.meitulu.com" + next_suffix_link
            yield scrapy.Request(next, callback=self.parse)

    # 具体的模特链接的解析方法
    def parse_img(self, response):
        item = MtlItem()
        item['no'] = response.xpath("//div[@class='c_l']/p[2]/text()").extract_first().split()[1]
        item['img_num'] = response.xpath("//div[@class='c_l']/p[3]/text()").extract_first().split()[1]
        # 这里还有一个小问题 有时p标签只有四个....
        item['user_name'] = response.xpath("string(//div[@class='c_l']/p[5])").extract_first().split('：')[1]

        try:
            item['img_date'] = response.xpath("//div[@class='c_l']/p[6]/text()").extract_first().split()[1]
        except:
            item['img_date'] = 'UNKnown'
        item['img_urls'] = response.xpath("//div[@class='content']/center//img/@src").extract()
        yield item
        # 下一页
        next_links = response.xpath("//center/div[@id='pages']/a/@href").extract()
        for next_suffix_link in next_links:
            next = "https://www.meitulu.com" + next_suffix_link
            yield scrapy.Request(next, callback=self.parse_img)
