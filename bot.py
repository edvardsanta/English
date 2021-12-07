# -- coding: utf-8 --
import settings 
import telebot
from telebot import types, apihelper
import re
from api import parser, client, english, error
bot = telebot.TeleBot(settings.API, parse_mode=None)
# You can set parse_mode by default. HTML or MARKDOWN

#Start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    print(message.chat.id)
    bot.reply_to(message, "Hello, i am an english bot")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, selective=True, row_width= 4)
    markup.add(types.KeyboardButton("Meaning"))
    markup.add("Transc")
    markup.add("Synonyms")
    text = "Welcome {}".format(message.from_user.first_name)
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Result1', types.InputTextMessageContent('hi'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('hi'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)

"""
#On generic text
@bot.message_handler(func=lambda m: True)
def generic(message):
    m_t = message.text
    if(m_t != "Synonyms" and m_t != "Transc" and m_t != "Meaning" and m_t != "/synonyms" and m_t != "/transc" and m_t != "/meaning"):
        text = "Click on menu and choose one function, please"
        bot.send_message(message.chat.id, text)
    else:
        next()
"""

#Transcription
@bot.message_handler(regexp = "[Tt]ransc")
def reg_message(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "Send me a word:", reply_markup=markup)
    bot.register_next_step_handler(message, word_text)
#Word transcription
def word_text(message):
    transcWord = message.text
    try:
        parser = client.fetch_parser(transcWord, english)       
        bot.reply_to(message, parser.get_transcription())
    except error:
        bot.reply_to(message, "There is no matching word in the list, sorry, type another word")

#Meaning
@bot.message_handler(regexp="[Mm]eaning")
def mean_message(message):
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, "Send me a word:", reply_markup=markup)
    bot.register_next_step_handler(message, mean_text)
#Word meaning
def mean_text(message):
    meanWord = message.text
    try:
        parser = client.fetch_parser(meanWord, english)
        bot.reply_to(message, parser.get_all_definitions())
    except error:
        bot.reply_to(message, "There is no matching word in the list, sorry, type another word")

#Synonyms
@bot.message_handler(regexp = "[Ss]ynonyms")
def syn_message(message):
    markup = types.ForceReply(selective=False)  
    bot.send_message(message.chat.id, "Send me a word:", reply_markup=markup)
    bot.register_next_step_handler(message, syn_text)
#Word synonyms
def syn_text(message):
    synWord = message.text
    try:
        parser = client.fetch_parser(synWord, english)
        all_synonyms: list[str] = parser.get_all_synonyms()
        all_synonyms.sort()
        all_synonyms = ", ".join(all_synonyms)
        bot.reply_to(message, f'All synonyms: \n{all_synonyms!r}')
    except error:
        bot.reply_to(message, "There is no matching word in the list, sorry, type another word ")
bot.infinity_polling()
client.close()

