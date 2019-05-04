import requests
from lxml import etree

class Books:
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}

    def __init__(self):
        pass

    @classmethod
    def search (cls,url):
        try:
            res = requests.get(url,headers=cls.headers,timeout=3)
        except requests.exceptions.RequestException as e:
            print(e)
            return {'error' : 'web request error'}
        content = res.content.decode()
        html = etree.HTML(content)
        title = html.xpath('//*[@id="searchlist"]/ul/li/h3/a/@title')
        price = html.xpath('//*[@id="searchlist"]/ul/li/span[@class="price"]/strong[not(contains(text(),"折"))]/b/text()')
        link = html.xpath('//*[@id="searchlist"]/ul/li/h3/a/@href')
        link = link = list(map(lambda x:'https:'+x,link))

        return {'title':"*－博客來－*\n",'data':zip(title,link,price)}

    @classmethod
    def search_books(cls,keyword):
        print('start searching {} in books'.format(keyword))
        return cls.search(f"http://search.books.com.tw/search/query/key/{keyword}/cat/all")

if __name__ == "__main__":
    pass