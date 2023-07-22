import scrapy
from ..items import MeituanminsuItem
import json
import openpyxl

class MttestSpider(scrapy.Spider):
    name = 'MTtest'
    allowed_domains = ['minsu.dianping.com']
    max_page = 17
    start_urls = ['https://minsu.dianping.com/']
    cookies_str = '_lxsdk_cuid=18019648522c8-0e956697dcb89e-48667e53-1bcab9-18019648522c8; _hc.v=52cce2f9-aefb-b062-d21d-885fa58d7090.1649693460; _ga=GA1.2.1734316872.1649693460; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _gid=GA1.2.563543224.1659282609; uuid=A5BF74F8C42B7A3F25C0C13ACC304C481B690A9C86DF68AB00201B1B6FE8E7C2; iuuid=A5BF74F8C42B7A3F25C0C13ACC304C481B690A9C86DF68AB00201B1B6FE8E7C2; zgwww=a3e87110-10e8-11ed-b2b7-8becf4169f75; zg.userid.untrusted=82772198; token2=U_uwFyrkHD_VXwm0PNsBH7mwdfMAAAAAQRMAANsRHCyQlkiA3uiz6QR3ikANwdOyKBue6Jc5QwXq93Fu6xeS9mKyub1XLIaNuDvbVw; userid=247019633; _lxsdk=A5BF74F8C42B7A3F25C0C13ACC304C481B690A9C86DF68AB00201B1B6FE8E7C2; _gat_gtag_UA_113236691_1=1; bottom-cover-closed=true; XSRF-TOKEN=Q4C2uTtC-R-1LlnnMjqtTn4C-4-ENTkfD8fA; _lxsdk_s=18254f341e3-b75-292-261%7C%7C41'
    cookies = {}
    for cookie in cookies_str.split(';'):
        key, value = cookie.split('=')
        cookies[key.strip()] = value.strip()

    def start_requests(self):
        # for minprice in range(44100, 100000, 3000):
        #     maxprice = minprice + 2000
        for page in range(1, 8):
            base_url = 'https://minsu.dianping.com/shanghai/pn{}/?minPrice={}&maxPrice={}&dateBegin=20220817&dateEnd=20220819'.format(page, 10000, 10500)
            yield scrapy.Request(base_url, callback=self.parse, cookies=self.cookies)


    def parse(self, response):
        all = response.xpath(".//div[@class='r-card-list__item shrink-in-sm']")
        for i in all:
            item = MeituanminsuItem()
            href = i.xpath('.//a[@class="product-card-container"]/@href').extract_first()
            item['room_id'] = href.split('/')[-2]
            item['title'] = i.xpath('./div/a/figure/figcaption/div/text()').extract_first('').replace('/', '_').replace("\\", '_').replace('|', '_').replace('\n', '_').replace('"', '_').replace("'", "_").replace('*', '_').replace(':', '_').replace('：', '_').replace('<', '_').replace('>', '_')
            item['place'] = i.xpath('./div/a/figure/figcaption/div/div[@class="mt-2"]/text()').extract_first('')
            item['price_latest'] = i.xpath('.//span[@class="product-card__price__latest"]/text()').extract_first('')
            item['price_original'] = i.xpath('.//del[@class="product-card__price__original"]/text()[2]').extract_first('')
            item['room'] = i.xpath('./div/a/figure/figcaption/div/div[1]/text()').extract_first('').split(' · ')[0]
            item['bed_num'] = i.xpath('./div/a/figure/figcaption/div/div[1]/text()').extract_first('').split(' · ')[1]
            item['capacity'] = i.xpath('./div/a/figure/figcaption/div/div[1]/text()').extract_first('').split(' · ')[2]
            item['likes'] = i.xpath('.//*[@class="product-fav-count"]/text()').extract_first()
            item['rating_nums'] = i.xpath('//*[@class="rating-num"]/text()').extract_first()
            room_url = response.urljoin(href)
            item['room_url'] = room_url

            yield scrapy.Request(url=room_url, cookies=self.cookies, callback=self.new_parse, meta={'item': item})


    def new_parse(self, response):
        item = response.meta['item']
        item['description1'] = response.xpath('//*[@id="J-specification"]/div[2]/div//text()').extract_first().replace('\r\n', '')
        item['tag_nums'] = len(response.xpath('//*[@id="J-nomalHouseTags"]/ul/li'))
        tag_names = []
        for i in response.xpath('//*[@id="J-nomalHouseTags"]/ul/li'):
            single_tag = i.xpath('./span/text()').extract_first()
            tag_names.append(single_tag)
        item['tag_names'] = ','.join(tag_names)
        item['host_name'] = response.xpath('//*[@id="J-host-info"]/section/div/div/div[1]/div/div/div[1]/a/text()').extract_first()
        item['avator_img'] = response.xpath('//*[@id="J-host-info"]/section/div/div/div[1]/div/a/img/@src').extract_first()
        item['host_realiability'] = response.xpath('//*[@id="J-host-item"]/section/div/div/div[1]/div/div/div[2]/text()').extract_first()
        item['super_host'] = response.xpath('//*[@id="J-host-info"]/section/div/div/div[2]/div/div[2]/div[1]/strong/text()').extract_first()
        item['avg_rate'] = response.xpath('//*[@id="productCommentsList"]/div[1]/div[1]/div[1]/text()').extract_first()
        item['score_des'] = response.xpath('//*[@id="productCommentsList"]/div[1]/ul/li[1]/div[1]/div/text()').extract_first()
        item['score_commu'] = response.xpath('//*[@id="productCommentsList"]/div[1]/ul/li[2]/div[1]/div/text()').extract_first()
        item['score_clean'] = response.xpath('//*[@id="productCommentsList"]/div[1]/ul/li[3]/div[1]/div/text()').extract_first()
        item['score_loc'] = response.xpath('//*[@id="productCommentsList"]/div[1]/ul/li[4]/div[1]/div/text()').extract_first()
        json_data = response.xpath('//script[@id="r-props-J-bookNotice"]//text()').extract_first().replace('<!--', '').replace('-->', '')
        page = json.loads(json_data)
        item['description2'] = ''.join(page.get('product').get('description'))
        item['aroundInfo'] = page.get('product').get('aroundInfo')
        item['productUserCount'] = page.get('product').get('productUserCount')
        item['commentNumber'] = page.get('product').get('commentNumber')
        item['extCommentNumber'] = page.get('product').get('extCommentNumber')
        item['longitude'] = page.get('product').get('addressInfo').get('longitude')
        item['bio'] = page.get('hostInfo').get('bio')
        item['replyTime'] = page.get('hostInfo').get('replyTime')
        item['productCount'] = page.get('hostInfo').get('productCount')
        item['goodCommentRate'] = page.get('hostInfo').get('goodCommentRate')
        item['hostCommentCount'] = page.get('hostInfo').get('commentCount')
        item['latitude'] = page.get('product').get('addressInfo').get('latitude')
        item['districtName'] = page.get('product').get('addressInfo').get('districtName')
        item['fullAddress'] = page.get('product').get('addressInfo').get('fullAddress')
        media_lists = page.get('product').get('productMediaInfoList')
        item['image_urls'] = []
        coverpage_urls = []
        bedroom_urls = []
        livingroom_urls = []
        bathroom_urls = []
        outdoor_urls = []
        list_mediaDesc = []
        for i in media_lists:
            pic_url = i.get('mediaUrl')
            mediaDesc = i.get('mediaDesc')
            mediaCategory = i.get('mediaCategory')
            if mediaCategory == 0:
                coverpage_urls.append(pic_url)
            if mediaCategory == 1:
                bedroom_urls.append(pic_url)
            if mediaCategory == 2:
                livingroom_urls.append(pic_url)
            if mediaCategory == 3:
                bathroom_urls.append(pic_url)
            if mediaCategory == 4:
                outdoor_urls.append(pic_url)
            list_mediaDesc.append(mediaDesc)

        item['image_urls'].append(coverpage_urls)
        item['image_urls'].append(bedroom_urls)
        item['image_urls'].append(livingroom_urls)
        item['image_urls'].append(bathroom_urls)
        item['image_urls'].append(outdoor_urls)
        item['mediaDesc'] = ','.join(list_mediaDesc)
        item['img_nums'] = len(item['image_urls'][0]) + len(item['image_urls'][1]) +len(item['image_urls'][2]) + len(item['image_urls'][3]) + len(item['image_urls'][4])

        yield item
