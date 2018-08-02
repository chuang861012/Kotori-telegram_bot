import json,requests,telegram,logging,re,os
from flask import Flask, jsonify, request
from modules.books import search_books
from modules.kings import search_kings
from modules.taaze import search_taaze
from modules.mugi import searchAuthor,getAuthorLinks,searchCircle,getCircleLinks
from modules.chat import getResponseText
from modules.hentai import searchRecommendHentai
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
            helpstr = ('/help - 指令清單\n'
                       '/author - 搜尋裏漫作者\n'
                       '/circle - 搜尋裏漫社團\n'
                       '/book - 搜尋書籍(博客來、金石堂、讀冊)\n'
                       '/huolu - 小鳥嚴選活路')
            bot.sendMessage(message.chat.id,helpstr)
        elif re.match('^/start',text):
            bot.sendMessage(message.chat.id,"現在並不是結束，結束甚至還沒有開始。但是現在可能是序幕的結束。\n - 溫斯頓·邱吉爾")
        elif re.match('^/author',text):
            bot.sendMessage(message.chat.id, "請輸入作者名",reply_markup=json.dumps({"force_reply":True}))
        elif re.match('^/circle',text):
            bot.sendMessage(message.chat.id, "請輸入社團名",reply_markup=json.dumps({"force_reply":True}))
        elif re.match('^/book',text):
            bot.sendMessage(message.chat.id, "請輸入ISBN或正確書名",reply_markup=json.dumps({"force_reply":True}))
        elif re.match('^/huolu',text):
            bot.sendMessage(message.chat.id, "小鳥嚴選活路")
            huolu(message)
        elif message.reply_to_message:
            if re.match('^請輸入作者名',message.reply_to_message.text):
                author(message,text)
            elif re.match('^請輸入社團名',message.reply_to_message.text):
                circle(message,text)
            elif re.match('^請輸入ISBN或正確書名',message.reply_to_message.text):
                book(message,text)
        else:
            res = getResponseText(text)
            bot.sendMessage(message.chat.id, res)

def author(message,text):
    author_data = searchAuthor(text)
    if author_data == None:
        bot.sendMessage(message.chat.id, "找不到作者 : *{}*".format(text),parse_mode="Markdown")
    elif 'error' in author_data:
        bot.sendMessage(message.chat.id,"Error : {}".format(author_data['error']))
    else:
        links = getAuthorLinks(author_data['_id'][1:],author_data['name'])
        if 'error' in links:
            bot.sendMessage(message.chat.id,"Error : {}".format(links['error']))
        else:
            if len(links) == 0:
                bot.sendMessage(message.chat.id, "作者 : *{}*，無相關資料".format(author_data['name']),parse_mode="Markdown")
            
            msgstr = "*{}*\n".format(author_data['name'])
            for item in links:
                msgstr += "[{}]({})\n".format(item[0],item[1])
            bot.sendMessage(message.chat.id,msgstr,parse_mode="Markdown")

def circle(message,text):
    circle_data = searchCircle(text)
    if circle_data == None:
        bot.sendMessage(message.chat.id, "找不到社團 : *{}*".format(text),parse_mode="Markdown")
    elif 'error' in circle_data:
        bot.sendMessage(message.chat.id,"Error : {}".format(circle_data['error']))
    else:
        links = getCircleLinks(circle_data['_id'][1:],circle_data['name'])
        if 'error' in links:
            bot.sendMessage(message.chat.id,"Error : {}".format(links['error']))
        else:
            msgstr = "*{}*\n成員 : ".format(circle_data['name'])
            for member in circle_data['member']:
                msgstr += member+" "
            msgstr += "\n"
            for item in links:
                msgstr += "[{}]({})\n".format(item[0],item[1])
            bot.sendMessage(message.chat.id,msgstr,parse_mode="Markdown")

def book(message,text):
    keyword = text
    books_res = list(search_books(keyword))
    kings_res = list(search_kings(keyword))
    taaze_res = list(search_taaze(keyword))
    if len(books_res)>0:
        result = parse_book_result(books_res,"*－博客來－*\n")
        bot.sendMessage(message.chat.id,result,parse_mode="Markdown",disable_web_page_preview=True)
    else:
        bot.sendMessage(message.chat.id,"博客來查無結果")
    if len(kings_res)>0:
        result = parse_book_result(kings_res,"*－金石堂－*\n")
        bot.sendMessage(message.chat.id,result,parse_mode="Markdown",disable_web_page_preview=True)
    else:
        bot.sendMessage(message.chat.id,"金石堂查無結果")
    if len(taaze_res)>0:
        result = parse_book_result(taaze_res,"*－讀冊－*\n")
        bot.sendMessage(message.chat.id,result,parse_mode="Markdown",disable_web_page_preview=True)
    else:
        bot.sendMessage(message.chat.id,"讀冊查無結果")

def huolu(message):
    result = searchRecommendHentai()
    if result == None:
        bot.sendMessage(message.chat.id,"沒有活路")
    elif 'error' in result:
        bot.sendMessage(message.chat.id,"Error : {}".format(result['error']))
    else:
        try:
            bot.sendPhoto(message.chat.id,photo=result['thumb'],caption='{}\n{}'.format(result['title'],result['link']))
        except:
            bot.sendMessage(message.chat.id,"活路不通 : telegram api timeout")
        

# home
@app.route('/')
def home():
    return "This is a python chat bot for telegram"

if __name__ == "__main__":
    app.run(debug=True)