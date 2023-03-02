
# https://stackoverflow.com/questions/33203645/how-to-plot-a-histogram-using-matplotlib-in-python-with-a-list-of-data
# https://www.geeksforgeeks.org/python-sort-list-elements-by-frequency/

import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def get_soup(url):
    # getting parseable webpage 
    req = Request(url, headers={'User-Agent': 'Brave/5.0'})
    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    soup = BeautifulSoup(webpage, "html.parser")
    return soup

def get_links(soup):
    links = []
    # finding links for ratings file 
    for link in soup.find_all('a'):
        try: 
            if len(link.get('href')) > 1: 
                try:
                    int(link.get('href')[1])
                    links.append("https://mydramalist.com" + link.get('href'))
                except ValueError:
                    continue 
                except TypeError:
                    continue
        except TypeError:
            continue
    return links

def get_titles(soup):
    # find titles for ratings file
    titles = []
    for title in soup.find_all('a'):
        if title.get('title') is not None:
            titles.append(title.get('title'))
        
    return titles

def get_my_ratings(soup):
    # find my ratings for ratings file 
    scores = []
    for score in soup.find_all('span'):
        if score.get('class') == ['score']:
            try: 
                scores.append(float(score.text[score.text.index(".") - 1:score.text.index(".") + 2]))
            except ValueError:
                scores.append(int(score.text))

    return scores


def getRating(url):
    # getting other peoples ave rating for ratings file 
    req = Request(url, headers={'User-Agent': 'Brave/5.0'})
    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    ratingIndex = webpage.find("ratingValue") + len("ratingValue:")
    try: 
        rating = float(webpage[ratingIndex + 1:ratingIndex + 4]) 
    except ValueError:
        rating = int(webpage[ratingIndex + 1])
    return rating

def get_recs(all_recs, soup):
    # pull all user recommendations 
    for rec in soup.find_all('a'):
        if rec.get('href') == "#":
            if rec.get('class') == ['text-primary', 'more-recs', 'text-primary']:
                start_index = rec.text.index('by') + 3
                end_index = start_index + 1
                while rec.text[end_index] != " ":
                    end_index += 1
                extra_recs = int(rec.text[start_index:end_index])
                while extra_recs > 0:
                    all_recs.append(all_recs[len(all_recs) - 1])
                    extra_recs -= 1
                # print("Extra recs: ", extra_recs)
        if rec.get('class') == ['text-primary']:
            try:
                int(rec.get('href')[1])
                all_recs.append("https://mydramalist.com" + rec.get('href')) 
            except TypeError:
                continue
            except ValueError:
                continue 

    return all_recs 


          
ratingsFile = open("/Users/sonajain/Desktop/Asian Movie Coding Project /ratings.txt", "w+")
# watchlistFile = open("/Users/sonajain/Desktop/Asian Movie Coding Project /watchlist.txt", "w+")
url = "https://mydramalist.com/dramalist/orangecoral"
soup = get_soup(url)
links = get_links(soup)
titles = get_titles(soup)
myRatings = get_my_ratings(soup)
# watchlistFile.writelines(webpage)

othRatings = [] 
rec_links = []
for link in links:
    # getting rec pages for each drama I've watched 
    othRatings.append(getRating(link))
    rec_link = link + "/recs"
    rec_links.append(rec_link)
    soup_rec = get_soup(rec_link)
    page_url = get_links(soup_rec)[len(get_links(soup_rec)) - 2] # seeing if >1 page of recs 
    try: 
        # print(len(page_url))
        page_num = int(page_url[len(page_url) - 1])
        while page_num > 1: 
            rec_links.append(rec_link + "?page=" + str(page_num))
            page_num -= 1
    except TypeError:
        continue  
    except ValueError:
        continue   

all_recs = []
for rec in rec_links:
    soup = get_soup(rec)
    all_recs = get_recs(all_recs, soup)

result = sorted(all_recs, key = all_recs.count,
                                reverse = True)
print("Final List:", result)

ratingDiff = []
for index in range(len(othRatings)):
    ratingDiff.append(round(myRatings[index] - othRatings[index],1))

for index in range(len(othRatings)):
    ratingsFile.writelines(str(titles[index]) + "," + 
                     str(myRatings[index]) + "," + 
                     str(othRatings[index]) + "," + 
                     str(links[index]) + '\n')
ratingsFile.close()
ratingsFile.close()




