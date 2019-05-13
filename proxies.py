import requests
import time
import threading
import queue
from lxml import etree

class thread_1(threading.Thread):
    """爬取西刺链接"""
    def __init__(self, threadName, pageQueue, dataQueue):
        threading.Thread.__init__(self)
        self.threadName = threadName  # 线程名字
        self.pageQueue = pageQueue  # 页码队列
        self.dataQueue = dataQueue  # 数据队列
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/73.0.3683.86 Safari/537.36'
                        }

    def run(self):
        print(self.threadName, '线程开始')
        while not self.pageQueue.empty():
            try:
                url ='https://www.xicidaili.com/nn/' + str(self.pageQueue.get())
                time.sleep(0.5)
                self.dataQueue.put(url)    # 把需要请求的url储存到队列
            except:
                print('队列错误')

        print(self.threadName, '线程结束')


class thread_2(threading.Thread):
    """解析含有ip信息的页面，并储存ip到本地"""
    def __init__(self, threadName, dataQueue, fileName):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.dataQueue = dataQueue
        self.fileName = fileName
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/73.0.3683.86 Safari/537.36'
                        }

    def run(self):
        print(self.threadName, '线程开始')
        while not self.dataQueue.empty():

            try:
                url = self.dataQueue.get()
                data = requests.get(url, headers=self.headers).text
                html = etree.HTML(data)
                ipdizhi = html.xpath('//tr[@class]/td[2]/text()')
                duankou = html.xpath('//tr[@class]/td[3]/text()')
                leixing = html.xpath('//tr[@class]/td[6]/text()')
                for i in range(len(ipdizhi)):
                    proxies = {leixing[i].lower(): leixing[i].lower() + '//' + ipdizhi[i] + ':' + duankou[i]}
                    time.sleep(0.5)
                    try:
                        response = requests.get('https://www.baidu.com', headers=self.headers, proxies=proxies)

                        # print(response)
                        if response.status_code == 200:
                            with open(self.fileName, 'a', encoding='utf-8') as f:
                                f.write(str(proxies) + '\n')  # 保存爬取的ip地址到本地
                    except:
                        print(i, ': 不可用')
            except:
                print('未知错误')

        print(self.threadName, '线程结束')


def main():
    # 创建需要爬取的页码队列
    pageQueue = queue.Queue()
    for i in range(1, 3):
        pageQueue.put(i)

    dataQueue = queue.Queue()   # 创建存储页面数据的队列
    pageurl = thread_1('采集线程', pageQueue, dataQueue)
    pageurl.start()
    pageurl.join()

    fileName = 'proxiesList.txt'
    proxies = thread_2('解析线程', dataQueue, fileName)
    proxies.start()
    proxies.join()

if __name__ == '__main__':
    main()
