# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class MeituRankDiyPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(url=item['img_url'],
                             meta={'model_name': item['model_name'],
                                   'model_score': item['model_score'],
                                   'album_head': item['album_head'], })

    def file_path(self, request, response=None, info=None, *, item=None):
        fn = r'rank_diy/%s/%s/%s' % (
            request.meta['model_name'] & request.meta['model_score'],
            request.meta['album_head'],
            request.url[-10:],
        )
        return fn
