import requests,urllib
from lxml import etree

class Kingstone:
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
        title = (html.xpath('//*[@id="mainContent"]/div/div/ul/li/a/span/text()'))
        price = (html.xpath('//span[@class="sale_price"]/em/text()'))
        link = html.xpath('//*[@id="mainContent"]/div/div/ul/li/a/@href')
        link = list(map(lambda x:'https://www.kingstone.com.tw'+x,link))

        return {'title':"*－金石堂－*\n",'data':zip(title,link,price)}

    @classmethod
    def search_kings(cls,keyword):
        print('start searching {} in kings'.format(keyword))
        keyword_list = urllib.parse.quote(keyword).split("%")
        keyword = "%25".join(keyword_list)
        return cls.search(f"https://www.kingstone.com.tw/search/result.asp?c_name={keyword}&se_type=4")

if __name__ == "__main__":
    pass