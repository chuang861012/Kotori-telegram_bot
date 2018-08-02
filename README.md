# Kotori Telegram_bot
A telegram chat bot written in python.
It's a chinese chat bot, english translation are in the comment.

# Installation
This bot is written in python(version 3.5). [install python](https://www.python.org/)

# Requiremants
List of required libraries to run the app
- **python-telegram-bot**
`$ pip install python-telegram-bot`
- **requests**
`$ pip install requests`
- **Flask**
`$ pip install Flask`
- **chatterbot**
`$ pip install chatterbot`
- **lxml**
`$ pip install lxml`

# Features
### Search about Dojinshi
dojinshi.org is a database of dojinshi. It provides an api for people to easily query it and get XML response.

Commands
```
/author
/circle
```
- Use `/author` to start searching dojinshi author.
- Use `/circle` to start searching dojinshi circle.

After typeing these command , the bot will ask you for the keyword you want to search.
Then get the best matched result and return useful links such as HomePage,Pixiv,Twitter.

The program first call the dojinshi api to get the id of the result.
Then scrape the webpage to get links.

### Search for books
Commands
```
/book
```
After typeing these command , the bot will ask you for the keyword you want to search.

The bot will scrape the three biggest online bookstore in Taiwan([books](http://www.books.com.tw/),[kingstone](https://www.kingstone.com.tw/),[taaze](http://www.taaze.tw/index.html)), get (up to) 5 results for each bookstore.
The result contains title, price, and the book's link.

### Get random manga from exhentai
Commands
```
/huolu
```
Use the command to get a manga from [exhentai](http://exhentai.org/) (A adult manga site).
The program will scrape a random page in exhentai, call [e-hentai api](https://ehwiki.org/wiki/API) to get gallery tags and filter the result using some rule.
Finally return the first gallery that pass the rule.

### Machine learning
This bot use [ChatterBot](https://github.com/gunthercox/ChatterBot) to chat with users.
ChatterBot is a machine-learning based conversational dialog engine build in Python.
Without typing any command. The bot will learn all the input text, and return the best response message.

The bot will save the learned response in database.
You can also train the bot with corpus packages.
example :
```
chatbot.train("chatterbot.corpus.english")
```
learn more : [ChatterBot Documentation](https://chatterbot.readthedocs.io/en/stable/)

### Other commands
```
/start
/help
```
- While first open the bot on telegram. You will be asked to type `/start`.
- Use `/help` to get command list.

# ToDo List
- more searching features
- inline bot

# License
Kotori bot is available under the MIT license.