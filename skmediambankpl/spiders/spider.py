import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import SkmediambankplItem
from itemloaders.processors import TakeFirst


class SkmediambankplSpider(scrapy.Spider):
	name = 'skmediambankpl'
	start_urls = ['https://sk.media.mbank.pl/']

	def parse(self, response):
		post_links = response.xpath('//a[contains(@class, "grid__box")]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@rel="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="pr-story-content"]//text()[normalize-space()]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="pr-story--date"]/p/text()').get()

		item = ItemLoader(item=SkmediambankplItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
