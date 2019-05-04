import requests,os
from lxml import etree

class Mugi:
    def __init__(self,APIKEY):
        self.APIKEY = APIKEY

    def searchAuthor(self,author):
        url = 'http://doujinshi.mugimugi.org/api/{}/?S=itemSearch&T=author&sn={}&order=jtitle'.format(self.APIKEY,author)
        try:
            res = requests.get(url,timeout=3)
        except requests.exceptions.RequestException as e:
            print(e)
            return {'error':'fetch mugi api error'}
        content = res.content
        tree = etree.XML(content)
        id_list = tree.xpath("//ITEM[@TYPE='author']/@ID")
        name_list = tree.xpath("//ITEM[@TYPE='author']/NAME_JP/text()")
        temp = ""
        if len(id_list)>0:
            for i in range(len(name_list)):
                if author.replace(" ", "").lower() == name_list[i].replace(" ", "").lower():
                    return {"_id":id_list[i],"name":name_list[i]}
                elif temp == "" and author.replace(" ", "").lower() in name_list[i].replace(" ", "").lower():
                    temp = {"_id":id_list[i],"name":name_list[i]}
            if temp != "":
                return temp
        else:
            return None

    def searchCircle(self,circle):
        url = 'http://doujinshi.mugimugi.org/api/{}/?S=itemSearch&T=circle&sn={}&order=jtitle'.format(self.APIKEY,circle)
        try:
            res = requests.get(url,timeout=3)
        except requests.exceptions.RequestException as e:
            print(e)
            return {'error':'fetch mugi api error'}
        content = res.content
        tree = etree.XML(content)
        items = tree.xpath("//ITEM[@TYPE='circle']")
        id_list = []
        name_list = []
        member_list = []
        for item in items:
            id_list.extend(item.xpath('@ID'))
            name_list.extend(item.xpath('NAME_JP/text()'))
            member_list.append(item.xpath('LINKS/ITEM[@TYPE="author"]/NAME_JP/text()'))
        temp = ""
        if len(id_list)>0:
            for i in range(len(name_list)):
                if circle.replace(" ", "").lower() == name_list[i].replace(" ", "").lower():
                    return {"_id":id_list[i],"name":name_list[i],"member":member_list[i]}
                elif temp == "" and circle.replace(" ", "").lower() in name_list[i].replace(" ", "").lower():
                    temp = {"_id":id_list[i],"name":name_list[i],"member":member_list[i]}
            if temp != "":
                return temp
        else:
            return None

    def getAuthorLinks(self,_id,name):
        url = 'https://www.doujinshi.org/browse/author/{}/{}/'.format(_id,name)
        return self.getLinks(url)

    def getCircleLinks(self,_id,name):
        url = 'https://www.doujinshi.org/browse/circle/{}/{}/'.format(_id,name)
        return self.getLinks(url)

    def getLinks(self,url):
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
        try:
            res = requests.get(url,headers=headers,timeout=3)
        except requests.exceptions.RequestException as e:
            print(e)
            return {'error':'web request error'}
        content = res.content.decode()
        html = etree.HTML(content)
        title = html.xpath('//table//tr/td/a[@class="OutGoingLink"]/@title')
        links = html.xpath('//table//tr/td/a[@class="OutGoingLink"]/@href')
        return list(zip(title,links))