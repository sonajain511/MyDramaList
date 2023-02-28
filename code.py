
# https://stackoverflow.com/questions/33203645/how-to-plot-a-histogram-using-matplotlib-in-python-with-a-list-of-data

import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import numpy as np
import matplotlib.pyplot as plt

def get_page(url):
    uClient = urlopen(url)
    website_text = uClient.read()
    uClient.close()
    soup = BeautifulSoup(website_text, "html.parser")
    # print(soup.p)
    containers = str(soup.find_all("div", {"class": "et_pb_text_inner"}))
    # print(containers)
    return containers

def remove_tags(html):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()

    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

def get_links(webpage):
    links = []
    titles = []
    scores = []
    soup = BeautifulSoup(webpage, "html.parser")

    # finding links 
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

    # find titles 
    for title in soup.find_all('a'):
        if title.get('title') is not None:
            titles.append(title.get('title'))

    # finding scores 

    for score in soup.find_all('span'):
        # print((score.get('class')))

        if score.get('class') == ['score']:
            try: 
                scores.append(float(score.text[score.text.index(".") - 1:score.text.index(".") + 2]))
            except ValueError:
                scores.append(int(score.text))
        
    return links, titles, scores 

def getRating(url):
    req = Request(url, headers={'User-Agent': 'Brave/5.0'})
    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    ratingIndex = webpage.find("ratingValue") + len("ratingValue:")
    try: 
        rating = float(webpage[ratingIndex + 1:ratingIndex + 4]) 
    except ValueError:
        rating = int(webpage[ratingIndex + 1])
    return rating
           
file1 = open("/Users/sonajain/Desktop/Asian Movie Coding Project /text_data1.txt", "w+")
url = "https://mydramalist.com/dramalist/orangecoral"
req = Request(url, headers={'User-Agent': 'Brave/5.0'})
web_byte = urlopen(req).read()
webpage = web_byte.decode('utf-8')
links, titles, myRatings = get_links(webpage)
# print(len(myRatings))

othRatings = [] 
for link in links:
    # print(link)
    othRatings.append(getRating(link))

ratingDiff = []
for index in range(len(othRatings)):
    ratingDiff.append(round(myRatings[index] - othRatings[index],1))

print("Rating Diff: ", ratingDiff)

'''
q25, q75 = np.percentile(ratingDiff, [25, 75])
bin_width = 2 * (q75 - q25) * len(ratingDiff) ** (-1/3)
bins = round((max(ratingDiff) - min(ratingDiff)) / bin_width)
print("Freedman–Diaconis number of bins:", bins)
plt.hist(ratingDiff, bins=bins)
'''

plt.scatter(myRatings, othRatings)
plt.show()

for index in range(len(othRatings)):
    file1.writelines(str(titles[index]) + "," + 
                     str(myRatings[index]) + "," + 
                     str(othRatings[index]) + "," + 
                     str(links[index]) + '\n')
file1.close()




