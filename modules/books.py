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
    title = html.xpath('//*[@id="searchlist"]/ul/li/h3/a/@title')
    price = html.xpath('//*[@id="searchlist"]/ul/li/span[@class="price"]/strong[not(contains(text(),"折"))]/b/text()')
    link = html.xpath('//*[@id="searchlist"]/ul/li/h3/a/@href')
    link = link = list(map(lambda x:'https:'+x,link))

    return zip(title,link,price)

def search_books(keyword):
    return search(f"http://search.books.com.tw/search/query/key/{keyword}/cat/all")
