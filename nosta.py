import os
import re
import time

import urllib2

ROOT = '/home/hill/Documents/nosta_crawler/pages/'


def get_page(url):
    url = url.replace('\'', '')
    content = dict()
    path = ROOT + url
    if os.path.exists(path):
        print path, 'exit'
        with open(path, 'r') as fp:
            content[url] = fp.read()
            return content
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; \
               Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    requests_num = 0


    while requests_num < 100:
        try:
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request, timeout=10)
            content[url] = response.read()

            dr = os.path.split(path)[0]
            fl = os.path.split(path)[1]
            if os.path.exists(path):
                print path, 'exit'
                return content
            if not os.path.exists(dr):
                os.makedirs(dr)
            with open(path, 'w') as fp:
                fp.write(content[url])

            return content
        except Exception as e:
            requests_num += 1
            print url
            if requests_num == 100:
                raise e
            time.sleep(10*requests_num)


def get_links(page):
    links = []
    for p, content in page.items():
        link_pattern = '.*?href=(.*?) target.*?'
        links_on_p = re.findall(link_pattern, content)
        print links_on_p
        # with open('page.html', 'w') as fp:
        #     print type(content)
        #     fp.write(content)
        # <IMG src='pic/title.jpg'>
        # print repr(content)
        # img_pattern = '.*IMG src=\'(.*)jpg\'.*'
        # img_on_p1 = re.findall(img_pattern, content)
        # print img_on_p1
        # img_pattern = '.*IMG src=\'(.*)jpg\'>.*'
        # img_on_p2 = re.findall(img_pattern, content)
        # print img_on_p2
        # # ><IMG src='../pic/000-2001/4-1.jpg' width='840px'>
        img_pattern = '.*?IMG src=\'(.*?)jpg\'.*?'
        img_on_p = re.findall(img_pattern, content, re.M)
        print img_on_p
        # img_on_p = img_on_p1 + img_on_p2 + img_on_p3
        # print img_on_p

        for img in img_on_p:
            links.append(os.path.join(os.path.split(p)[0],
                                      img + 'jpg'.replace('\'', '')))
        for link in links_on_p:
            links.append(os.path.join(os.path.split(p)[0],
                                      link.replace('\'', '')))
    return links


if __name__ == '__main__':
    root = '/home/hill/Documents/nosta_crawler/pages/'
    url = 'http://www.nosta.gov.cn/upload/2018slxmgb/showProject.html'
    # url = 'http://www.nosta.gov.cn/upload/2018slxmgb/zr_101/zrIndex.html'
    # url = 'http://www.nosta.gov.cn/upload/2018slxmgb/zr_101/000-2001.html'
    links = [url]
    i = 0
    while links != []:
        for link in links:
            with open('links.txt', 'a+') as fp:
                fp.write('    ' * i + link + '\n')
        i += 1
        pages = []
        for url in links:
            pages.append(get_page(url))
        links = []
        for page in pages:
            links.extend(get_links(page))
    print(links)
