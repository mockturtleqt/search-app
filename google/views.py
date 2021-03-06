from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
import html2text
from urllib2 import urlopen
import nltk
from .models import URL, Keyword
from bs4 import BeautifulSoup


# def add_url(request):
#     url = request.GET.get('q')
#     (url)
#     return

def get_all_urls(request):
    urls = URL.objects.all()
    return render(request, "google/urls.html", {'urls': urls})


def homepage(request):
    return render(request, "google/homepage.html")


def search(request):
    #query = str()
    query = request.GET["query"]
    if "query" in request.GET:
        matched_urls = get_list_or_404(URL, keyword__keyword=query)
        #query = request.GET["query"].split()
        #query = query.split()
        #matched_urls = URL.objects.filter(keyword__keyword=request.GET["query"])
        if matched_urls:
            return render(request, "google/homepage.html", {"urls": matched_urls})

            #return HttpResponse(matched_urls)


def lookup(word):
    matched_urls = URL.objects.filter(keyword__keyword=word)
    if matched_urls:
        return matched_urls
    else:
        return "There are no urls matching your query"


def index_page(request):
    url = request.GET["index"]
    if "index" in request.GET:
        content = get_content(url)
        #return HttpResponse(get_content(url)) #prints content
        add_page_to_index(url, content)
        w = Keyword.objects.all()
        # u = URL.objects.all()
        return HttpResponse(w)
        #return HttpResponse(get_page(url)) # jumps to requested page

        #return render(request, "google/search_results.html", {"urls": url})


def get_content(url):
    try:
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_emphasis = True
        h.skip_internal_links = True
        link = get_page(url)
        #soup = BeautifulSoup(link)
        #return soup.get_text()
        result = h.handle(link.decode("utf-8"))
        return result.encode("ascii", "ignore")
    except:
        return None


def add_page_to_index(url, content):
    words = nltk.word_tokenize(content[:100])
    for word in words:
        add_to_index(word, url)


def get_page(url):
    try:
        return urlopen(url).read()
    except:
        return None


def add_to_index(keyword, url):
    requested_url = URL.objects.filter(url=url).first()
    if requested_url is None:
        requested_url = URL.objects.create(url=url)
    requested_word = requested_url.keyword_set.filter(keyword__icontains=keyword).first()
    if requested_word is None:
        requested_word = Keyword.objects.create(keyword=keyword)
    requested_word.urls.add(requested_url)
    requested_word.save()

"""def search(request):
    #kword = Keyword.objects.get(keyword__exact)

    if "query" in request.GET:
        message = URL.objects.filter(keyword__keyword=request.GET["query"])
    #    if lookup(url, request.GET["query"]):
        #message = 'You submitted: %r' % request.GET["query"]

    else:
        message = 'You submitted nothing!'
    return HttpResponse(message)

    def lookup(index, keyword):
    for entry in index:
        if entry[0] == keyword:
            return entry[1][0]
    return []"""

# def get_content(url):
#     try:
#         h = html2text.HTML2Text()
#         h.ignore_links = True
#         h.ignore_links = True
#         h.ignore_emphasis = True
#         h.skip_internal_links = True
#         link = get_page(url)
#         result = h.handle(link.decode("utf-8"))
#         return result.encode("ascii", "ignore")
#     except:
#         return


# def record_user_click(index, keyword, url):
#     urls = lookup(index, keyword)
#     if urls:
#         for entry in urls:
#             if entry[0] == url:
#                 entry[1] += 1
#
#
# def add_to_index(index, keyword, url):
#     for entry in index:
#         if entry[0] == keyword:
#             for urls in entry[1]:
#                 if urls[0] == url:
#                     return
#             entry[1].append(url, 0)
#             return
#     index.append([keyword, [url, 0]])


# def add_to_index(index, keyword, url):
#     u = URL.objects.filter(url=url).first()
#     if u is None:
#         u = URL.objects.create(url=url)
#     w = Keyword.objects.filter(keyword=keyword).first()
#     if w is None:
#         w = Keyword.objects.create(keyword=keyword)
#     w.urls.add(u)
#     w.save()

    # for entry in index:
    #     if entry[0] == keyword:
    #         for urls in entry[1]:
    #             if urls == url:
    #                 return
    #         entry[1].append(url)
    #         return
    # index.append([keyword, [url]])

    # requested_word = Keyword.objects.filter(keyword=keyword)
    # if requested_word is None:
    #     requested_word = Keyword.objects.create(keyword=keyword, url__urls=url)
    # requested_url = requested_word.url__urls_set.filter(url__urls=url)
    # if requested_url is None:
    #     requested_url = URL.objects.create(url=url)
    # requested_word.url.add(requested_url)
    # requested_word.save()


# def split(source):
#     output = []
#     at_split = True
#     splitlist = " .,!?"
#     for char in source:
#         if char in splitlist:
#             at_split = True
#         else:
#             if at_split:
#                 output.append(char)
#                 at_split = False
#             else:
#                 output[-1] = output[-1] + char
#     return output





# def get_next_target(page):
#     start_link = page.find('<a href=')
#     if start_link == -1:
#         return None, 0
#     start_quote = page.find('"', start_link)
#     end_quote = page.find('"', start_quote + 1)
#     url = page[start_quote + 1:end_quote]
#     return url, end_quote


# def union(p, q):
#     for e in q:
#         if e not in p:
#             p.append(e)


# def get_all_links(page):
#     links = []
#     while True:
#         url, endpos = get_next_target(page)
#         if url:
#             links.append(url)
#             page = page[endpos:]
#         else:
#             break
#     return links


# def crawl_web(seed, max_depth):
#     tocrawl = [seed]
#     crawled = []
#     index = []
#     depth = 0
#     next_depth = []
#     while tocrawl and depth <= max_depth:
#         page = tocrawl.pop()
#         if page not in crawled:
#             content = get_content(page)
#             add_page_to_index(index, page, content)
#             union(next_depth, get_all_links(get_page(page)))
#             crawled.append(page)
#         if not tocrawl:
#             tocrawl, next_depth = next_depth, []
#             depth += 1
#     return index



# print crawl_web("http://www.bbc.com/earth/story/20160607-monkey-stone-age-secrets-unveiled", 1)
# crawl_web("http://mashable.com/2016/06/09/wwdc-2016-what-to-expect/?utm_cid=hp-hh-pri#Z5mIJRUSziqm", 0)

#get_page('http://python.org/')
#print get_page("http://www.bbc.com/earth/story/20160607-monkey-stone-age-secrets-unveiled")




