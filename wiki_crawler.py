#!/usr/bin/env python
import urllib
import re
from BeautifulSoup import BeautifulSoup

def get_random_wiki():
    response = urllib.urlopen('http://en.wikipedia.org/wiki/Special:Random')
    return response.geturl()

def invalidUrl(input):
    if input.find('Wikipedia:') != -1:
        return 1
    if input.find('index.php') != -1:
        return 1
    if input.find('#') != -1:
        return 1
    if input.find('.png') != -1:
        return 1
    if input.find('.svg') != -1:
        return 1
    if input.find('.jpg') != -1:
        return 1
    if input.find('.gif') != -1:
        return 1
    if input.find(':') != -1:
        return 1
    if input.find('upload') != -1:
        return 1
    return 0

def del_parentheses_from_content(content):
    prundedContent = re.sub("[\(\[].*?[\)\]]?!^<a>*?</a>", "", str(content))
    return BeautifulSoup(prundedContent)

class wiki_article(object):
    def __init__(self, url):
        self.current_article = url
        self.first_link = url
        self.goal = 'Philosophy'
        self.visited = []

    def set_current_article(self, wiki_url):
            self.current_article = wiki_url

    def set_first_link(self, wiki_url):
        self.first_link = wiki_url

    def add_to_visited(self, wiki_url):
        self.visited.append(wiki_url)

    def get_current_article(self):
        return self.current_article

    def get_first_link(self):
        return self.first_link

    def get_visited_articles(self):
        return self.visited, len(self.visited)

    def evaluate_goal(self):
        current_link = self.get_current_article().split("/wiki/")
        if current_link[1] == self.goal:
            return True
        else:
            return False

    #Grab first link on the main body of the article that is not within parenthesis or italicized.
    def find_first_link(self):
        response = urllib.urlopen(self.current_article)
        print 'Evaluating current article: {}'.format(response.geturl())
        html = response.read()
        soup = BeautifulSoup(html) #Parse html
        content = soup.findAll('div',attrs={'id':'mw-content-text','class':'mw-content-ltr'})

        for div in content:
            paragarphs = div.findAll('p')
            for paragraph in paragarphs:
                paren_free = del_parentheses_from_content(paragraph) #Rm all content within parens. Links EXCLUDED.
                links = paren_free.findAll('a')
                for link in links:
                    if link.parent.name != "i" and invalidUrl(link['href']) == 0: #Iterate until proper link found.
                        self.add_to_visited('http://en.wikipedia.org{}'.format(link['href']))
                        return 'http://en.wikipedia.org{}'.format(link['href']) #First non-italic link found out of parens.

def main():
    start_wiki = get_random_wiki()
    start_page_name = start_wiki.split("/wiki/")[1]
    if start_page_name == 'Philosophy':
        print 'Wiki article, {} was randomly selected and matches our goal!'.format(start_wiki)
        return

    wiki = wiki_article(start_wiki)
    while wiki.evaluate_goal() is False:
        first_acceptable_link = wiki.find_first_link()
        wiki.set_current_article(first_acceptable_link)

    if wiki.evaluate_goal() is True:
        articles, article_count = wiki.get_visited_articles()
        print 'Goal! Philosophy successfully reached by clicking on {} first links found.'.format(article_count)
        print 'Report Path'
        for article in articles:
            print article
        return
    else:
        print 'Something very bad happened here but I assure you I tested this thoroughly.'

if __name__ == '__main__':
    main()