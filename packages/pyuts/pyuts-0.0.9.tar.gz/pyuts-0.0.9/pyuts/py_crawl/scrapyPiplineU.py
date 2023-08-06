# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB
from ..py_db.mongoDBU import MongoDBU


class ScrapyPiplineU(PyApiB):
    """
    scrapyPipline相关封装工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def __init__(self):
        from scrapy.utils.project import get_project_settings
        settings = get_project_settings()
        host = settings["MONGO_HOST"]
        port = settings["MONGO_PORT"]
        user = settings["MONGO_USER"]
        pswd = settings["MONGO_PSWD"]
        self.dbname = settings["MONGO_DB_NAME"]
        # 创建MONGODB数据库链接
        self.client = MongoDBU().init(host, port, user, pswd)

    def process_item(self, item, spider):
        data = dict(item)
        # self.post.insert(data)
        tb_name = item.saveTableName
        if tb_name == None:
            tb_name = item.__class__.__name__
        self.client.upsert_one(self.dbname, tb_name, {'id': data['id']}, data)
        return item

    def getDB(self) -> MongoDBU:
        return self.client

    def getDBName(self):
        return self.dbname

    def open_spider(self, spider):
        spider.myPipline = self
        spider.state = 'running'

    def close_spider(self, spider):
        spider.myPipline = None
        spider.state = 'close'