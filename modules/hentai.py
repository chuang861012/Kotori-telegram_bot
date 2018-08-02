import requests,random,os
from time import sleep
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Cookie": os.environ.get('HENTAI_COOKIE') # EXHENTAI COOKIE
}

rules = {
    "rape": 2,
    "blackmail": 23, #
    "schoolgirl uniform": 22, #
    "sole female": 0.5, 
    "sex toys": 2,
    "exhibitionism": 23, #
    "mind break": 1.5,
    "mind control":1.5,
    "filming": 22, #
    "chikan": 1.5,
    "lolicon": 22, #
    "swimsuit":0.5,
    "school swimsuit":1,
    "bunny girl":21, #
    "bdsm":1,
    "stockings":0.5,
    "defloration":1,
    "elf":21.5, #
    "slave":1,
    "cunnilingus":1,
    "inverted nipples":1,
    "fingering":1,
    "masturbation":1.5
}

def search(url):
    print('searching :',url)
    try:
        res = requests.get(url, headers=headers,timeout=3)
    except requests.exceptions.RequestException as e:
        print(e)
        return {'error':'web request error'}
    print('request to exhentai page :',res.status_code)
    if res.status_code != 200:
        return {'error':'web response error'}
    content = res.content.decode()
    html = etree.HTML(content)
    links = html.xpath('/html/body/div/div[2]/div[2]/div/div[1]/a/@href')
    gidlist = []
    for link in links:
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
            if tag in rules:
                score += rules[tag]
        if score > 24.5:
            return {'title':gallery['title'],'link':'https://exhentai.org/g/{}/{}/'.format(gallery["gid"], gallery["token"]),'thumb':gallery["thumb"]}

    next_page = html.xpath(
        '/html/body/div/div[2]/table[1]//tr/td/a[contains(text(),">")]/@href')
    if len(next_page) <= 0 or next_page[0] == "#":
        return None
    else:
        sleep(.1)
        return search(next_page[0])

def searchRecommendHentai():
    print('start getting gallery')
    page = random.randint(0,5000)
    result = search("https://exhentai.org/?page={}".format(page))
    print('gallery got, start return response')
    return result


if __name__ =='__main__':
    result = searchRecommendHentai()
    print(result)
