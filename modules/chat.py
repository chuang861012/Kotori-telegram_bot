import os
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chatbot = ChatBot(
    'Ron Obvious',
    trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri=os.environ.get('DATABASE_URL','./database.sqlite3')
)

# # 簡中語言庫
# chatbot.train("chatterbot.corpus.chinese")

# chatbot.set_trainer(ListTrainer)
# chatbot.train(conversation)

def getResponseText(string):
    text = chatbot.get_response(string).text
    return text