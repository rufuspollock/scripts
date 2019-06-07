#!/usr/bin/env python
# TODO: use beautiful soup or HTML tidy
# import twill.commands as web
import os
import urllib
from HTMLParser import HTMLParser

def imdb_search_url(name):
        baseurl = 'http://www.imdb.com/'
        quoted = urllib.quote(name)
        url = baseurl + 'find' + '?q=%s' % quoted
        return url

def external_reviews(filmid):
    url = baseurl + 'title/%s/' % filmid
    page = urllib.urlopen(url)
    page.read()


class GetLinks(HTMLParser):

    def reset(self):
        HTMLParser.reset(self)
        self.links = []
        self.text = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = ''
            for at in attrs:
                if at[0] == 'href':
                    href = at[1]
                    break
            self.links.append(['', href])
            self.text = ''

    def handle_endtag(self, tag):
        if tag == 'a':
            self.links[-1][0] = self.text

    def handle_data(self, text):
        cleantext = text.strip()
        self.text += cleantext

    def title_links(self):
        def istitle(link):
            href = link[1]
            return href.startswith('/title/tt')
        results = filter(istitle, self.links) 
        return results

    def reviews(self):
        my_reviewers = [
                'Roger Ebert, Chicago Sun-Times',
                'Guardian/Observer',
                'BBCi - Films',
                'metacritic.com - Reviews and Scores from Leading Film Critics',
                ]
        def wanted(link):
            return link[0] in my_reviewers
        return filter(wanted, self.links)

def search_imdb(name):
    url = imdb_search_url(name)
    print url
    fo = urllib.urlopen(url)
    # if a single result will auto-redirect
    if fo.url.startswith('http://www.imdb.com/title/tt'): # straight to title
        # expect relative urls ...
        href = fo.url[19:36]
        return [ [ name, href] ]
    content = fo.read()
    fo.close()
    getlinks = GetLinks()
    try:
        getlinks.feed(content)
    except: # lots of bad html
        pass
    links = getlinks.title_links()
    return links

def get_reviews(url):
    fo = urllib.urlopen(url)
    content = fo.read()
    fo.close()
    getlinks = GetLinks()
    getlinks.reset()
    try:
        getlinks.feed(content)
    except Exception, inst: # lots of bad html
        print 'Link parser barfed: %s' % inst
    links = getlinks.reviews()
    return links

class TestStuff:

    def test_0(self):
        name = 'kingdom'
        url = imdb_search_url(name)
        assert name in url

    def test_1(self):
        # url = 'http://www.imdb.com/title/tt0053779/'
        url = 'http://www.imdb.com/find?q=la+dolce+vita'
        fo = urllib.urlopen(url)
        content = fo.read()
        fo.close()
        getlinks = GetLinks()
        try:
            getlinks.feed(content)
        except:
            # lots of bad html
            pass
        links = getlinks.title_links()
        print links
        assert len(links) == 17
        assert links[0][0] == 'Dolce vita, La'

    def test_reviews(self):
        url = 'http://www.imdb.com/title/tt0053779/externalreviews'
        links = get_reviews(url)
        print links
        assert len(links) == 4

    def test_reviews_4(self):
        # fails because link parser barfs
        url = 'http://www.imdb.com/title/tt0408839/externalreviews'
        links = get_reviews(url)
        print links
        assert len(links) == 4

def main():
    name = raw_input('Search for: ')
    # TODO: some films have only one result and therefore auto-redirect ...
    links = search_imdb(name)
    for ii in range(len(links)):
        print ii, ':', links[ii][0]
    choice = raw_input('Choose film number: ')
    choice = int(choice)
    url = 'http://www.imdb.com' + links[choice][1]
    print choice, url
    reviews_url = url + 'externalreviews'
    print reviews_url
    reviews = get_reviews(reviews_url)
    for ii in range(len(reviews)):
        print ii, ': ', reviews[ii][0]
    to_view = raw_input('Select reviews (e.g. 1,3,5): ')
    to_view = to_view.split(',')
    to_view = [ int(ii) for ii in to_view ]
    for ii in range(len(to_view)): 
        rev_url = reviews[to_view[ii]][1]
        cmd = 'w3m -no-cookie %s' % rev_url
        os.system(cmd)
    # do_another = raw_input('Do another? (y/n): ') 

if __name__ == '__main__':
    main()
