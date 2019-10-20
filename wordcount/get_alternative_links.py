import pandas as pd
import newspaper
from googlesearch import search
import pdb
import argparse
import tldextract
from datetime import timedelta
from . import softCosine
import requests
import io
import numpy as np


def get_url_bias(url, corpus):
 
    try:
        return corpus.loc[corpus['source_url_processed'].str.contains(tldextract.extract(url).domain)]['bias'].values[0]
    except IndexError:
        return 'center'
    
def get_url_fact(url, corpus):
    try:
        return corpus.loc[corpus['source_url_processed'].str.contains(tldextract.extract(url).domain)]['fact'].values[0]
    except IndexError:
        return 'MIXED'
    
def get_search_query(url):

    article = newspaper.Article(url)

    article.download()
    article.parse()
    article.nlp()

    query             = article.title
    
    try:
        date_before       = article.publish_date + timedelta(days=2)
        date_after        = article.publish_date - timedelta(days=2)

        query_time_before = str(date_before.year) +\
                            '-' + str(date_before.month) +\
                            '-' + str(date_before.day)

        query_time_after = str(date_after.year) +\
                            '-' + str(date_after.month) +\
                            '-' + str(date_after.day)
        
        query = query + ' before:' + query_time_before + ' after:' + query_time_after
    
    except TypeError:
        
        print('Date for the article not available. Finding other articles across all times')

    return query
    

    
def get_query_results(search_query):
    
    alt_article_lists = [i for i in search(search_query, num = 10)]
    search_results_df = pd.DataFrame(columns = ['link', 'domain', 'title', 'content'])

    search_results_df['link'] = alt_article_lists
    search_results_df['domain'] = search_results_df['link'].apply(lambda x: tldextract.extract(x).domain\
                                                                             + '.' + tldextract.extract(x).suffix)
    
    return search_results_df

def get_summary(url):

    article = newspaper.Article(url)
    article.download()
    article.parse()
    article.nlp()
    return article


def get_alternative_links(url):

    corpus_url   = 'https://raw.githubusercontent.com/Omairss/BeyondBias/master/data/corpus.csv'
    s            = requests.get(corpus_url).content
    corpus       = pd.read_csv(io.StringIO(s.decode('utf-8')))

    url_bias      = get_url_bias(url, corpus)
    url_fact      = get_url_fact(url, corpus)
    query         = get_search_query(url)

    try:

        search_results_df = pd.read_csv(query)

    except IOError:

        print('file not found')
    
        
        query_results_df = get_query_results(query)
        query_results_df = query_results_df.fillna('')


        search_results_df = pd.merge(corpus, query_results_df, left_on = 'source_url_processed', right_on = 'domain')
        search_results_df = search_results_df[~search_results_df['bias'].str.replace('-', ' ').str.contains(url_bias)]
        
        search_results_df['cosine_similarity'] = search_results_df['link'].apply(lambda x: softCosine.getSimilarity(x, url))

        ## Filtering by custom score
        search_results_df['score'] = search_results_df['cosine_similarity']/np.log(np.array(search_results_df.index) + 1)
        #search_results_df = search_results_df.loc[search_results_df['score'] > 0.2]
        
        try:
            search_results_df['content'] = search_results_df['link'].apply(lambda x: get_summary(x).summary)
            search_results_df['title'] = search_results_df['link'].apply(lambda x: get_summary(x).title)
        except:
            pass
    
    search_results_df.to_csv(query, index = False)
    
    return search_results_df.reset_index().sort_values('score', ascending = False).to_dict(orient = 'index')