from django.http import HttpResponse
from django.shortcuts import render
from .get_alternative_links import get_alternative_links
from wordcount.bellsAndWhistles import *

def homepage(request):
    return render(request, 'index.html')
    

def classify(request):
    url = str(request.GET['url'])
    links = get_alternative_links(url)
    returnList=[]

    for key in list(links.keys()):
        returnList.append((links[key]['link'],links[key]['title'],links[key]['content'],links[key]['fact'],links[key]['bias']))
    
    #return render(request, 'index.html', {'links': links_list})
    #{'links': {"link": ["google.com","amazon.com","facebook.com"], "title" : ["facebook","amazon","google"]}}
    #gayasData=[(getReadTime(),getToneScore(),links)]
    results={'links': {"link": returnList}}
    return render(request, 'index.html', context=results)