#!/usr/bin/python3

# coding: utf-8

# !Py3.5.2

# # Anime Profile Pic Scraper
# 
# A bot to: 
# 1. Cycle through all the characters in https://myanimelist.net starting from https://myanimelist.net/character/1 ;
# 2. For each character, navigate to its pictures page eg https://myanimelist.net/character/1/Spike_Spiegel/pictures * (as a side note, I could perhaps search instead for https://myanimelist.net/character/1/<???>/pictures) *
# 3. Scrape all links to the profile pictures
# 4. Create a new folder with the ID + Profile name of the Character (collaborator)
# 5. Save all pictures in this new folder (collaborator)
# 6. Repeat (collaborator)
# 
# ## How will it do each step?
# 
# 1. Character IDs are incremental - we can simply start from https://myanimelist.net/character/1 and then add 1 until we receive an error; As a failsafe, consider saving the enumerator in an outside text file.
# 2. Two possible methods using bs4:
#     1. Scrape link to the pages by navigating to its position on the page
#     2. Search each `<a>` tag on the page for https://myanimelist.net/character/1/<???>/pictures
# 3. Use bs4 to create a list of all the links * (idea, how about using a <a href="https://docs.python.org/3.3/tutorial/datastructures.html"><strong>set rather than a list</strong></a>? Sets naturally check for duplicates and eliminate them - thus ensuring a picture is not downloaded twice). *
# 4. It should be easy to scrape the name from either the original character page or the character page. Then use the os module to create a new folder with the id and the name.
# 5. Cycle through the set created in step 3. and download the pictures. A good option to do this is `urllib.request.urlretrieve()` (<a href='https://stackoverflow.com/a/8286449'>see here for reference</a>)
# 6. Print out confirmation message, add 1 to the enumerator, and repeat.

#dependencies
from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve

link_prefix = "https://myanimelist.net"


# ## Step 1: 
# * Cycle through all the characters in https://myanimelist.net starting from https://myanimelist.net/character/1
# * Character IDs are incremental - we can simply start from https://myanimelist.net/character/1 and then add 1 until we receive an error. 
# * As a failsafe, **consider saving the enumerator in an outside text file**.



#while True: #uncomment this for production and indent everything below



# starting up
character_id = 1

# create a link
character_page_url = "https://myanimelist.net/character/"+str(character_id)+"/"
character_page_html = urlopen(character_page_url, timeout=30)
#print(character_page_html.info()) #remove for production




#create a Beautiful Soup object
character_soup = BeautifulSoup(character_page_html, "html.parser")
#print(soup.prettify()) #remove for production


# ## Step 2:
# 
# * For each character, navigate to its pictures page eg https://myanimelist.net/character/1/Spike_Spiegel/pictures
# * Two possible methods using bs4:
#     1. Scrape link to the pages by navigating to its position on the page
#     2. Search each `<a>` tag on the page for https://myanimelist.net/character/1/<???>/pictures



# Method 1:

#the link is enclosed in a div with the id content, so find that div
div = character_soup.find(id="content")

#the link is invariably the first a tag in the div content - so find that
#get('href') returns the href value of the <a> tag, i.e. the url we are looking for
a_tag_href = div.a.get('href')

#join the url with the prefix to make it valid
pictures_url = link_prefix+a_tag_href
print(pictures_url)

# Method 2: 
# couldn't get this to work - but this seems more complicated than method one, which seems to work just fine
#a_tags =character_soup.find_all("a")
#for a_tag in a_tags:
#    a_tag_link = a_tag.get('href')
#    if a_tag_link != None and a_tag_link.startswith("https"):
#        split = a_tag_link.split("/")
#        if split[-1] == "pictures":
#            print(a_tag_link) 


# ## Step 3:
# 
# * open a soup object to the profile pictures page
# * Scrape all links to the profile pictures
# * Use bs4 to create a list of all the links * (idea, how about using a
# <a href="https://docs.python.org/3.3/tutorial/datastructures.html"><strong>set rather than a list</strong></a>?
# Sets naturally check for duplicates and eliminate them - thus ensuring a picture is not downloaded twice). *

pictures_html = urlopen(pictures_url, timeout=30)
pictures_soup = BeautifulSoup(pictures_html, "html.parser")
#print(pictures_soup.prettify()) #remove for production

pictures_div = pictures_soup.find(id="content")

tables_list = pictures_div.find_all("table")
picture_tags_set = set(tables_list[3].find_all("img"))
picture_urls = set()
for picture in pictures_set:
    picture_url = picture.get("src")
    picture_urls.add(picture_url)

# ## Step 4: Saving
# 
# As per instructions:
# "and you collect the image urls, make a dict from url to character ids, and url to character name"
# 
# hint given:
# 
# `unique_char_names = set(blablabla)
# char_names_to_char_ids = dict(zip(unique_char_names, [i for i in range(len(unique_char_names)])`

#get character name
character_name = pictures_soup.find("meta", property="og:title").get("content")

#make dict from url to character id
url_to_char_id = dict()
url_to_char_name = dict()

#if there is a better way to do this... I don't know what it is
for url in picture_urls:
    url_to_char_id[url] = character_id
    url_to_char_name[url] = character_name

for key, value in url_to_char_id.items():
    print("{}: {}".format(key, value))
for key, value in url_to_char_name.items():
    print("{}: {}".format(key, value))    

