# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import scrapy
from scrapy.pipelines.images import ImagesPipeline


class MeituModelPipeline(ImagesPipeline):
    def get_media_requests(self, t, info):
        yield scrapy.Request(
            url=t['img_url'],
            meta={
                'mo': t['model_origin'],
                'mn': t['model_name'],
                'ah': t['album_head'],
            },
        )

    def file_path(self, request, response=None, info=None, *, item=None):
        fn = r'result-model/%s/%s/%s/%s' % (request.meta['mo'], request.meta['mn'], request.meta['ah'], request.url[-8:])
        return fn
