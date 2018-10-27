import multiprocessing
from scrapy import cmdline

'''启动指定Spider'''
# cmdline.execute("scrapy crawl ArtistSpider".split())
'''启动所有Spider'''
cmdline.execute("scrapy crawlall".split())


'''
基于进程池启动多个Spider
'''
# def spider_execute():
#     cmdline.execute("scrapy crawlall".split())
#
#
# class Execute:
#     @staticmethod
#     def run(processes_num):
#         pool = multiprocessing.Pool(processes=processes_num)
#
#         pool.apply_async(spider_execute)
#         pool.close()
#         pool.join()
#
#
# if __name__ == '__main__':
#     Execute.run(10)
