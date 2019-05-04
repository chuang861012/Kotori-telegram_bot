import requests,random,os,json
from time import sleep
from lxml import etree

tagDict = None

with open('res/tagdata.json', 'r') as f:
    tagDict = json.load(f)

class Hentai:
    def __init__(self,cookie):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Cookie": cookie
        }

    def getGalleryPage(self,url):
        print('searching :',url)
        try:
            res = requests.get(url, headers=self.headers,timeout=3)
        except requests.exceptions.RequestException as e:
            print(e)
            return {'error':'web request error'}
        print('request to exhentai page :',res.status_code)
        if res.status_code != 200:
            return {'error':'web response error'}
        content = res.content.decode()
        html = etree.HTML(content)
        nodes = html.xpath('//div[contains(@class,"glname")]//a')
        next_page = html.xpath(
            '/html/body//tr/td/a[contains(text(),">")]/@href')
        return {'nodes':nodes,'next_page':next_page}

    def search(self,url):
        page = self.getGalleryPage(url)
        if 'error' in page:
            return page
        gidlist = []
        for node in page['nodes']:
            link = node.xpath('@href')[0]
            gidlist.append([link.split("/")[4], link.split("/")[5]])

        try:
            res = requests.post("https://api.e-hentai.org/api.php",
                                json={
                                    "method": "gdata",
                                    "gidlist": gidlist,
                                    "namespace": 0
                                },timeout=3)
        except requests.exceptions.RequestException as e:
            print(e)
            return {'error':'fetch e-hentai api request error'}
        print('calling exhentai api :',res.status_code)
        if res.status_code != 200:
            return {'error':'fetch e-hentai api response error'}

        for gallery in res.json()["gmetadata"]:
            score = 0
            for tag in gallery["tags"]:
                if tag in tagDict:
                    score += tagDict[tag]
            if score > 3.708694940232474:
                return {'title':gallery['title'],'link':'https://exhentai.org/g/{}/{}/'.format(gallery["gid"], gallery["token"]),'thumb':gallery["thumb"]}

        next_page = page['next_page']
        if len(next_page) <= 0 or next_page[0] == "#":
            return None
        else:
            sleep(.1)
            return self.search(next_page[0])

    def favorites(self,url):
        page = self.getGalleryPage(url)
        if 'error' in page:
            return page
        gidlist = []
        picked = random.choice(page['nodes'])
        link = picked.xpath('@href')[0]
        gidlist.append([link.split("/")[4], link.split("/")[5]])

        try:
            res = requests.post("https://api.e-hentai.org/api.php",
                                json={
                                    "method": "gdata",
                                    "gidlist": gidlist,
                                    "namespace": 0
                                },timeout=3)
        except requests.exceptions.RequestException as e:
            print(e)
            return {'error':'fetch e-hentai api request error'}
        print('calling exhentai api :',res.status_code)
        if res.status_code != 200:
            return {'error':'fetch e-hentai api response error'}

        data = res.json()["gmetadata"]
        if len(data) != 1:
            return {'error':'data error'}
        
        return {'title':data[0]['title'],'link':'https://exhentai.org/g/{}/{}/'.format(data[0]["gid"], data[0]["token"]),'thumb':data[0]["thumb"]}

    def getFavPage(self):
        print('getting fav page num')
        try:
            res = requests.get('https://exhentai.org/favorites.php', headers=self.headers,timeout=3)
        except requests.exceptions.RequestException as e:
            print(e)
            return 'error'
        print('request to exhentai page :',res.status_code)
        if res.status_code != 200:
            return 'error'
        content = res.content.decode()
        html = etree.HTML(content)
        page = html.xpath('//table[@class="ptt"]//td[last()-1]/a/text()')[0]
        return page

    def searchRecommendHentai(self):
        print('start getting gallery')
        page = random.randint(0,5000)
        result = self.search("https://exhentai.org/?page={}".format(page))
        print('gallery got, start return response')
        return result

    def getMyFavorites(self):
        page = self.getFavPage()
        if page == 'error':
            print('fail to get fav page')
            return {'error':'fail to get fav page'}
        page = random.randint(0,int(page))
        return self.favorites('https://exhentai.org/favorites.php?page={}'.format(page))