import html2text
from urllib2 import urlopen
import nltk
#nltk.download('all')
import unicodedata

#h = html2text.HTML2Text()
#h.ignore_links = True
#result = h.handle(get_page("http://www.bbc.com/earth/story/20160607-monkey-stone-age-secrets-unveiled").decode('utf-8'))
#unicodedata.normalize('NFKD', result).encode('ascii','ignore')
#print result.encode('utf-8')
#print unicodedata.normalize('NFKD', result).encode('ascii','ignore')
#print result.encode('ascii', 'ignore')


def get_content(url):
    try:
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_links = True
        h.ignore_emphasis = True
        h.skip_internal_links = True
        link = get_page(url)
        result = h.handle(link.decode("utf-8"))
        return result.encode("ascii", "ignore")
    except:
        return


def get_page(url):
    try:
        return urlopen(url).read()
    except:
        return

"""

def record_user_click(index, keyword, url):
    urls = lookup(index, keyword)
    if urls:
        for entry in urls:
            if entry[0] == url:
                entry[1] += 1


def add_to_index(index, keyword, url):
    for entry in index:
        if entry[0] == keyword:
            for urls in entry[1]:
                if urls[0] == url:
                    return
            entry[1].append(url, 0)
            return
    index.append([keyword, [url, 0]])"""


def add_to_index(index, keyword, url):
    for entry in index:
        if entry[0] == keyword:
            for urls in entry[1]:
                if urls == url:
                    return
            entry[1].append(url)
            return
    index.append([keyword, [url]])


def lookup(index, keyword):
    for entry in index:
        if entry[0] == keyword:
            return entry[1][0]
    return []


"""def split(source):
    output = []
    at_split = True
    splitlist = " .,!?"
    for char in source:
        if char in splitlist:
            at_split = True
        else:
            if at_split:
                output.append(char)
                at_split = False
            else:
                output[-1] = output[-1] + char
    return output
"""


def add_page_to_index(index, url, content):
    #words = content.split()
    #words = split(content)
    words = nltk.word_tokenize(content)
    for word in words:
        add_to_index(index, word, url)


def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote


def union(p, q):
    for e in q:
        if e not in p:
            p.append(e)


def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def crawl_web(seed, max_depth):
    tocrawl = [seed]
    crawled = []
    index = []
    depth = 0
    next_depth = []
    while tocrawl and depth <= max_depth:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_content(page)
            add_page_to_index(index, page, content)
            union(next_depth, get_all_links(get_page(page)))
            crawled.append(page)
        if not tocrawl:
            tocrawl, next_depth = next_depth, []
            depth += 1
    return index


print crawl_web("http://www.bbc.com/earth/story/20160607-monkey-stone-age-secrets-unveiled", 1)
# crawl_web("http://mashable.com/2016/06/09/wwdc-2016-what-to-expect/?utm_cid=hp-hh-pri#Z5mIJRUSziqm", 0)

#get_page('http://python.org/')
#print get_page("http://www.bbc.com/earth/story/20160607-monkey-stone-age-secrets-unveiled")



