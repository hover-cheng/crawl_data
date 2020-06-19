import urllib.request
import json
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
import ssl
import os
import csv

# python3 访问https的url是需要添加以下代码
ssl._create_default_https_context = ssl._create_unverified_context
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def getItemId(item, pagenum, filename):
    itemname = urllib.request.quote(item)
    url = "https://search.jd.com/Search?keyword=%s&enc=utf-8&page=%d" % (itemname, pagenum)
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
    referer = "https://www.jd.com/"
    res = urllib.request.Request(url, headers={"user-agent": userAgent, "referer": referer})
    rep = urllib.request.urlopen(res)
    bsObj = BeautifulSoup(rep, 'html.parser', from_encoding="gb18030")
    rep.close()
    items = bsObj.findAll('li', {'class': 'gl-item'})
    for i in items:
        itemTitle = i.find('div', {'class': 'p-name p-name-type-2'}).em.get_text().strip('\n\t').strip()
        itemUrl = i.a.attrs['href']
        itemPrice = i.i.get_text().strip()
        filename.writerow((itemTitle, "https:" + itemUrl, itemPrice))


def main(itemlist, pagenum):
    for item in itemlist:
        FILE_NAME = os.path.join(BASE_DIR, 'jd_%s.csv') % item
        csvfile = open(FILE_NAME, 'w+', newline='', encoding='gb18030')
        filewrite = csv.writer(csvfile)
        filewrite.writerow(("title", "url", "price"))
        pool = ThreadPool(processes=10)
        for i in range(pagenum):
            pool.apply_async(getItemId, (item, i, filewrite))
        pool.close()
        pool.join()


if __name__ == "__main__":
    itemlist = ['固态硬盘', '苹果手机', '华为手机']
    main(itemlist, 10)
