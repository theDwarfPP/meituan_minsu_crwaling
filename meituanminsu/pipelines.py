# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import time

from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import openpyxl

class MeituanminsuPipeline:
    def process_item(self, item, spider):
        return item

class ExcelPrintPipeline(object):
    def process_item(self, item, spider):
        wb = openpyxl.load_workbook('chachong.xlsx')
        ws = wb.active
        data = []
        data.append(item['title'])
        data.append(item['place'])
        data.append(item['price_latest'])
        data.append(item['price_original'])
        data.append(item['likes'])
        data.append(item['rating_nums'])
        data.append(item['room'])
        data.append(item['bed_num'])
        data.append(item['capacity'])
        data.append(item['room_url'])
        data.append(item['room_id'])
        data.append(item['img_nums'])
        data.append(item['description1'])
        data.append(item['tag_nums'])
        data.append(item['tag_names'])
        data.append(item['host_name'])
        data.append(item['avator_img'])
        data.append(item['host_realiability'])
        data.append(item['super_host'])
        data.append(item['avg_rate'])
        data.append(item['score_des'])
        data.append(item['score_commu'])
        data.append(item['score_clean'])
        data.append(item['score_loc'])
        data.append(item['description2'])
        data.append(item['aroundInfo'])
        data.append(item['longitude'])
        data.append(item['latitude'])
        data.append(item['districtName'])
        data.append(item['fullAddress'])
        data.append(item['mediaDesc'])
        data.append(item['productUserCount'])
        data.append(item['extCommentNumber'])
        data.append(item['commentNumber'])
        data.append(item['bio'])
        data.append(item['replyTime'])
        data.append(item('productCount'))
        data.append(item('goodCommentRate'))
        data.append(item('hostCommentCount '))

        ws.append(data)
        wb.save('chachong.xlsx')
        return item



class MTPicturePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
         for i in item['image_urls']:
             for image_url in i:
                yield scrapy.http.Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        item = request.meta['item']
        image_num = request.url.split('/')[-1]
        if request.url in item['image_urls'][0]:
            file_name = '.\\{}\\{}\\{}'.format(item['title'], 0, item['title'] + image_num)
        if request.url in item['image_urls'][1]:
            file_name = '.\\{}\\{}\\{}'.format(item['title'], 1, item['title'] + image_num)
        if request.url in item['image_urls'][2]:
            file_name = '.\\{}\\{}\\{}'.format(item['title'], 2, item['title'] + image_num)
        if request.url in item['image_urls'][3]:
            file_name = '.\\{}\\{}\\{}'.format(item['title'], 3, item['title'] + image_num)
        if request.url in item['image_urls'][4]:
            file_name = '.\\{}\\{}\\{}'.format(item['title'], 4, item['title'] + image_num)

        return file_name

