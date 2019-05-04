import json,requests,telegram,logging,re,os,threading
from flask import Flask, jsonify, request
from modules.books import Books
from modules.kings import Kingstone
from modules.taaze import Taaze
from modules.mugi import Mugi
from modules.chat import getResponseText
from modules.hentai import Hentai
from modules.av import Av
from modules.utils import parse_book_result

app = Flask(__name__)
token = os.environ.get('TELEGRAM_TOKEN') # telegram bot token
bot_name = "@KimikaKotori_bot"
bot = telegram.Bot(token=token)
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@app.route('/webhook', methods=['POST'])
def launcher():
    update = telegram.Update.de_json(request.get_json(force=True),bot)
    handle_message(update.message)
    return 'ok'

def handle_message(message):
    print(message)
    text = message.text
    if text:
        if re.match('^/help',text):
            helpstr = ('*Hentai*\n'
                       '/author - 搜尋裏漫作者\n' #search for adult manga author
                       '/circle - 搜尋裏漫社團\n' #search for adult manga circle
                       '/huolu - 小鳥嚴選活路\n' # get random adult manga
                       '/myfav - 小鳥專業推薦\n'
                       '/av - 小鳥認清現實\n'
                       '*Book*\n'
                       '/book - 搜尋書籍(博客來、金石堂、讀冊)\n' # search for books in bookstore(books,kingstone,taaze)
                       '*About*\n'
                       '/help - 指令清單\n' # command list
                       '/source - Github repository link')
            bot.sendMessage(message.chat.id,helpstr,parse_mode="Markdown")
        elif re.match('^/source',text):
            bot.sendMessage(message.chat.id,'[Github](https://github.com/chuang861012/Kotori-telegram_bot)',parse_mode="Markdown")
        elif re.match('^/start',text):
            bot.sendMessage(message.chat.id,"現在並不是結束，結束甚至還沒有開始。但是現在可能是序幕的結束。\n - 溫斯頓·邱吉爾") # a random string
        elif re.match('^/author',text):
            bot.sendMessage(message.chat.id, "請輸入作者名",reply_markup=json.dumps({"force_reply":True})) # please enter the author's name
        elif re.match('^/circle',text):
            bot.sendMessage(message.chat.id, "請輸入社團名",reply_markup=json.dumps({"force_reply":True})) # please enter the circle's name
        elif re.match('^/book',text):
            bot.sendMessage(message.chat.id, "請輸入ISBN或正確書名",reply_markup=json.dumps({"force_reply":True})) # please enter the ISBN or name of the book
        elif re.match('^/av',text):
            bot.sendMessage(message.chat.id, "請輸入番號 / 關鍵字",reply_markup=json.dumps({"force_reply":True})) # please enter the ISBN or name of the book
        elif re.match('^/huolu',text):
            bot.sendMessage(message.chat.id, "小鳥嚴選活路") # random adult manga
            huolu(message)
        elif re.match('^/myfav',text):
            bot.sendMessage(message.chat.id, "小鳥專業推薦") # random adult manga
            myfav(message)
        elif message.reply_to_message:
            if message.reply_to_message.text:
                if re.match('^請輸入作者名',message.reply_to_message.text):
                    author(message,text)
                elif re.match('^請輸入社團名',message.reply_to_message.text):
                    circle(message,text)
                elif re.match('^請輸入ISBN或正確書名',message.reply_to_message.text):
                    book(message,text)
                elif re.match('^請輸入番號 / 關鍵字',message.reply_to_message.text):
                    avgle(message,text)
            else:
                pass
        elif re.match('^!',text):
            pass
        else:
            res = getResponseText(text)
            bot.sendMessage(message.chat.id, res)

def author(message,text):
    mugi_spider = Mugi(os.environ.get('MUGI_APIKEY'))
    author_data = mugi_spider.searchAuthor(text)
    if author_data == None:
        bot.sendMessage(message.chat.id, "找不到作者 : *{}*".format(text),parse_mode="Markdown") # can't find author
    elif 'error' in author_data:
        bot.sendMessage(message.chat.id,"Error : {}".format(author_data['error']))
    else:
        links = mugi_spider.getAuthorLinks(author_data['_id'][1:],author_data['name'])
        if 'error' in links:
            bot.sendMessage(message.chat.id,"Error : {}".format(links['error']))
        else:
            if len(links) == 0:
                bot.sendMessage(message.chat.id, "作者 : *{}*，無相關資料".format(author_data['name']),parse_mode="Markdown") # author has no link
            
            msgstr = "*{}*\n".format(author_data['name'])
            for item in links:
                msgstr += "[{}]({})\n".format(item[0],item[1])
            bot.sendMessage(message.chat.id,msgstr,parse_mode="Markdown")

def circle(message,text):
    mugi_spider = Mugi(os.environ.get('MUGI_APIKEY'))
    circle_data = mugi_spider.searchCircle(text)
    if circle_data == None:
        bot.sendMessage(message.chat.id, "找不到社團 : *{}*".format(text),parse_mode="Markdown") # can't find circle
    elif 'error' in circle_data:
        bot.sendMessage(message.chat.id,"Error : {}".format(circle_data['error']))
    else:
        links = mugi_spider.getCircleLinks(circle_data['_id'][1:],circle_data['name'])
        if 'error' in links:
            bot.sendMessage(message.chat.id,"Error : {}".format(links['error']))
        else:
            msgstr = "*{}*\n成員 : ".format(circle_data['name']) # member
            for member in circle_data['member']:
                msgstr += member+" "
            msgstr += "\n"
            for item in links:
                msgstr += "[{}]({})\n".format(item[0],item[1])
            bot.sendMessage(message.chat.id,msgstr,parse_mode="Markdown")

def book(message,text):
    keyword = text

    results = []

    def job(keyword,func):
        res = func(keyword)
        results.append(res)

    books_threading =  threading.Thread(target=job,args=(keyword,Books.search_books))
    kings_threading =  threading.Thread(target=job,args=(keyword,Kingstone.search_kings))
    taaze_threading =  threading.Thread(target=job,args=(keyword,Taaze.search_taaze))
    books_threading.start()
    kings_threading.start()
    taaze_threading.start()
    books_threading.join()
    kings_threading.join()
    taaze_threading.join()

    for res in results:
        if 'error' in res:
            bot.sendMessage(message.chat.id,"Error : {}".format(res['error']))
        else:
            result = parse_book_result(list(res['data']),res['title'])
            bot.sendMessage(message.chat.id,result,parse_mode="Markdown",disable_web_page_preview=True)

def huolu(message):
    hentai = Hentai(os.environ.get('HENTAI_COOKIE'))
    result = hentai.searchRecommendHentai()
    print(result)
    if result == None:
        bot.sendMessage(message.chat.id,"沒有活路") # no result
    elif 'error' in result:
        bot.sendMessage(message.chat.id,"Error : {}".format(result['error']))
    else:
        try:
            bot.sendPhoto(message.chat.id,photo=result['thumb'],caption='{}\n{}'.format(result['title'],result['link']))
        except:
            bot.sendMessage(message.chat.id,"活路不通 : telegram api timeout") # error

def myfav(message):
    hentai = Hentai(os.environ.get('HENTAI_COOKIE'))
    result = hentai.getMyFavorites()
    if 'error' in result:
        bot.sendMessage(message.chat.id,"Error : {}".format(result['error']))
    else:
        try:
            bot.sendPhoto(message.chat.id,photo=result['thumb'],caption='{}\n{}'.format(result['title'],result['link']))
        except:
            bot.sendMessage(message.chat.id,"活路不通 : telegram api timeout") # error

def avgle(message,text):
    result = Av.get(text)
    if 'error' in result:
        bot.sendMessage(message.chat.id,"Error : {}".format(result['error']))
    else:
        try:
            bot.sendPhoto(message.chat.id,photo=result['thumb'],caption='{}\n{}\n還有另外 {} 個結果。'.format(result['title'],result['link'],result['total']))
        except:
            bot.sendMessage(message.chat.id,"Error : telegram api timeout") # error

# home
@app.route('/')
def home():
    return "This is a python chat bot for telegram"

if __name__ == "__main__":
    app.run(debug=True)