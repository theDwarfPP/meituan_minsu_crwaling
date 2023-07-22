# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituanminsuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    place = scrapy.Field()
    price_latest = scrapy.Field()
    price_original = scrapy.Field()
    likes = scrapy.Field()
    rating_nums = scrapy.Field()
    room = scrapy.Field()
    bed_num = scrapy.Field()
    capacity = scrapy.Field()
    room_url = scrapy.Field()
    room_id = scrapy.Field()
    img_nums =scrapy.Field()
    description1 = scrapy.Field()
    tag_nums = scrapy.Field()
    tag_names = scrapy.Field()
    host_name = scrapy.Field()
    avator_img = scrapy.Field()
    host_realiability = scrapy.Field()
    super_host = scrapy.Field()
    avg_rate = scrapy.Field()
    score_des = scrapy.Field()
    score_commu = scrapy.Field()
    score_clean = scrapy.Field()
    score_loc = scrapy.Field()
    productUserCount = scrapy.Field()
    commentNumber = scrapy.Field()
    bio = scrapy.Field()
    replyTime = scrapy.Field()
    productCount = scrapy.Field()
    goodCommentRate = scrapy.Field()
    hostCommentCount = scrapy.Field()
    extCommentNumber = scrapy.Field()
    description2 = scrapy.Field()
    aroundInfo = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    districtName = scrapy.Field()
    fullAddress = scrapy.Field()
    image_urls = scrapy.Field()
    mediaDesc = scrapy.Field()


