#!/usr/bin/python

import datetime
import PyRSS2Gen
import requests
import xmlpp
from BeautifulSoup import BeautifulSoup

def main():
    url = 'http://mobile.twitter.com/ckuijjer/favorites'
    response = requests.get(url)

    soup = BeautifulSoup(response.content)

    rss_items = []
    tweets = soup.findAll('table', { 'class': 'tweet' })

    for tweet in tweets:
        author = tweet.find('strong', { 'class': 'fullname' }).text
        username = tweet.find('span', { 'class': 'username' }).text
        content = tweet.find('div', { 'class': 'dir-ltr' })
        tweet_id = tweet.find('td', { 'class': 'timestamp' }).find('a')['name']

        links = content.findAll('a')
        first_link = None
        for link in links:
            href = link.get('data-url') or link.get('href')

            if href.startswith('/'):
                href = 'https://www.twitter.com' + href

            link['href'] = href

            if not first_link and not href.startswith('https://www.twitter.com'):
                first_link = href


        description = '<a href="https://www.twitter.com/%s">%s - %s</a><br/>%s' % (username, username, author, content)

        rss_items.append(PyRSS2Gen.RSSItem(
            title = content.text,
            link = first_link,
            description = description,
            pubDate = datetime.datetime.now(),
            guid = PyRSS2Gen.Guid(tweet_id, isPermaLink = 0)
            ))


    rss = PyRSS2Gen.RSS2(
            title = 'Starred Tweets',
            link = 'http://home.kuijjer.com/starred_tweets.rss',
            description = 'Starred Tweets',
            lastBuildDate = datetime.datetime.now(),
            items = rss_items,
            )

    print xmlpp.get_pprint(rss.to_xml())

if __name__ == "__main__":
    main()
