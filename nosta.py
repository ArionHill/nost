import os
import re
import time

import urllib2

ROOT = '/home/hill/Documents/nosta_crawler/pages/'


def get_page(url):
    url = url.replace('\'', '')
    print 'get_page: ', url
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


    while requests_num < 10:
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
            print 'done'
            return content
        except Exception as e:
            requests_num += 1
            print url
            if requests_num == 100:
                raise e
            time.sleep(2**requests_num)


def get_links(page):
    print 'get_links'
    links = []
    for p, content in page.items():
        # *('.*href=(.*) target.*')是贪婪匹配，在不影响后续匹配是否成功的前提下*会一直匹配下去，所以只能找到一行中的最后一个字符串;
        # 改为非贪婪的*？('.*?href=(.*?) target.*?')就可以找到到所有符合条件的字符串
        link_pattern = '.*?href=(.*?) target.*?'
        links_on_p = re.findall(link_pattern, content)
        img_pattern = '.*?IMG src=\'(.*?)jpg\'.*?'
        img_on_p = re.findall(img_pattern, content, re.M)
        for img in img_on_p:
            links.append(os.path.join(os.path.split(p)[0],
                                      img + 'jpg'.replace('\'', '')))
        for link in links_on_p:
            links.append(os.path.join(os.path.split(p)[0],
                                      link.replace('\'', '')))
    print 'done'
    return links


if __name__ == '__main__':
    root = '/home/hill/Documents/nosta_crawler/pages/'
    url = 'http://www.nosta.gov.cn/upload/2018slxmgb/showProject.html'

    links = [url]
    i = 0
    while links != []:
        print 'links != []'
        for link in links:
            with open('links.txt', 'a+') as fp:
                fp.write('    ' * i + link + '\n')
        i += 1
        pages = []
        for url in links:
            pages.append(get_page(url))
        links = []
        for page in pages:
            print 'page'
            links.extend(get_links(page))
    print 'DONE'
