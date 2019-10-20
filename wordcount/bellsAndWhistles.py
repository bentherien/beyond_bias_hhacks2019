from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from newspaper import Article
import requests
from bs4 import BeautifulSoup
def getReadTime(body):
    wc = len(body.split())
    return wc/200
def getToneScore(body):
    opinion = TextBlob(body)
    sentiment = opinion.sentiment.polarity
    return int(sentiment*100)
def getSourceScore(article):
    html = article.html
    text = article.text
    #get number of long quotes
    nq = text.count("\"")/2
    #get number of links
    nl = html.count("<a href")
    returnVal=nq+nl
    return (str(returnVal*5)+"%")
if __name__ == '__main__':
    url = 'https://www.newyorker.com/books/page-turner/how-jane-vonnegut-made-kurt-vonnegut-a-writer'
    article = Article(url)
    article.download()
    article.parse()
    print(article.authors)
    article.nlp()
    print(article.keywords)
    authors=""
    print(getToneScore(article.text))
    print(str(getReadTime(article.text))+" minutes")
    print(getSourceScore(article))
