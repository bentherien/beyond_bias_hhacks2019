from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from newspaper import Article
import requests
from bs4 import BeautifulSoup



def getCosine(body_1, body_2, title_1, title_2):
    
    bodies = (body_1, body_2)
    titles = (title_1, title_2)
    
    tfidf_vectorizer = TfidfVectorizer()
    
    tfidf_matrix_bodies = tfidf_vectorizer.fit_transform(bodies)
    tfidf_matrix_titles = tfidf_vectorizer.fit_transform(titles)
    
    cosine_similarity_bodies=(cosine_similarity(tfidf_matrix_bodies[0:1], tfidf_matrix_bodies[1]))[0][0]
    cosine_similarity_titles=(cosine_similarity(tfidf_matrix_titles[0:1], tfidf_matrix_titles[1]))[0][0]
    
    return 0.5*(cosine_similarity_bodies+cosine_similarity_titles)


def getSimilarity(url1, url2):
    
    #url1 = 'https://www.newyorker.com/books/page-turner/how-jane-vonnegut-made-kurt-vonnegut-a-writer'
    #url2 = 'https://www.nytimes.com/2007/04/12/books/12vonnegut.html'
    
    article1 = Article(url1)
    article2 = Article(url2)
    
    article1.download()
    article2.download()
    
    article1.parse()
    article2.parse()
    
    body1=article1.text
    body2=article2.text
    
    title1=article1.title
    title2=article2.title
    
    return getCosine(body1, body2, title1, title2)