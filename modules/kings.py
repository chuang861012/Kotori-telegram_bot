import requests,urllib
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
    title = (html.xpath('//*[@id="mainContent"]/div/div/ul/li/a/span/text()'))
    price = (html.xpath('//span[@class="sale_price"]/em/text()'))
    link = html.xpath('//*[@id="mainContent"]/div/div/ul/li/a/@href')
    link = list(map(lambda x:'https://www.kingstone.com.tw'+x,link))

    return zip(title,link,price)

def search_kings(keyword):
    keyword_list = urllib.parse.quote(keyword).split("%")
    keyword = "%25".join(keyword_list)
    return search(f"https://www.kingstone.com.tw/search/result.asp?c_name={keyword}&se_type=4")