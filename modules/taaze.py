import requests
from lxml import etree

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}

def search (url):
    try:
        res = requests.get(url,headers=headers,timeout=3)
    except requests.exceptions.RequestException as e:
        print(e)
        return ['error : web request error']
    content = res.content.decode()
    html = etree.HTML(content)
    items = html.xpath('/html/body/div[5]/div[2]/div[4]/div/div[2]/ul/li[@class="linkC"][not(contains(text(),"(二手書)"))]/..')
    title = []
    price = []
    link = []
    for item in items:
        title.extend(item.xpath('li[@class="linkC"]/a/text()'))
        price.extend(item.xpath('li[5]/span[last()]/span[last()]/text()'))
        link.extend(item.xpath('li[@class="linkC"]/a/@href'))

    return zip(title,link,price)

def search_taaze(keyword):
    return search(f"https://www.taaze.tw/search_go.html?keyword%5B%5D={keyword}&keyType%5B%5D=0&prodKind=0&prodCatId=0&catId=0&salePriceStart=&salePriceEnd=&saleDiscStart=0&saleDiscEnd=0&publishDateStart=&publishDateEnd=&prodRank=0&addMarkFlg=0")
