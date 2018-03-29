import os
import re

import urllib2


def get_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US;\
               rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    requests_num = 0
    content = dict()
    while requests_num < 3:
        try:
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request, timeout=10)
            content[url] = response.read()
            return content
        except Exception as e:
            raise e
            requests_num += 1


def get_links(page):
    links = []
    for p, content in page.items():
        link_pattern = '.*href=(.*) target.*'
        links_on_p = re.findall(link_pattern, content)
        with open('page.html', 'w') as fp:
            print type(content)
            fp.write(content)
        # <IMG src='pic/title.jpg'>
        print repr(content)
        img_pattern = '.*IMG src=\'(.*)jpg\'.*'
        img_on_p1 = re.findall(img_pattern, content)
        print img_on_p1
        img_pattern = '.*IMG src=\'(.*)jpg\'>.*'
        img_on_p2 = re.findall(img_pattern, content)
        print img_on_p2
        # ><IMG src='../pic/000-2001/4-1.jpg' width='840px'>
        img_pattern = '.*?IMG src=\'(.*?)jpg\'.*?'
        img_on_p3 = re.findall(img_pattern, content, re.M)
        print img_on_p3
        img_on_p = img_on_p1 + img_on_p2 + img_on_p3
        print img_on_p
        for img in img_on_p:
            links.append(os.path.join(os.path.split(p)[0], img + 'jpg'))
        for link in links_on_p:
            links.append(os.path.join(os.path.split(p)[0], link))
    return links


if __name__ == '__main__':
    root = '/home/hill/Documents/nosta_crawler/pages/'
    url = 'http://www.nosta.gov.cn/upload/2018slxmgb/showProject.html'
    # url = 'http://www.nosta.gov.cn/upload/2018slxmgb/zr_101/000-2001.html'
    page = get_page(url)
    links = get_links(page)
    print(links)
