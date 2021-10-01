import os
import json
import requests
import io
from bs4 import BeautifulSoup
from PIL import Image
from tqdm import tqdm 
from genericpath import exists

MANGA_URL = 'https://berserkonline.com/manga/berserk-chapter'
BASE_URL = 'https://berserkonline.com'
LINKS_FILE = 'manga_links.json'

'''
Checks if there's a json containing the manga links
if there isn't, it gets the links using the web crawler
and then saves them as a json
'''
def readLinks():
    if exists(LINKS_FILE) and os.stat(LINKS_FILE).st_size > 0:
        jsonFile = open(LINKS_FILE,'r')
        links = json.load(jsonFile)
        jsonFile.close()
        return links
    else:
        links = getLinks()
        jsonFile = open(LINKS_FILE,'w')
        json.dump(links, jsonFile)
        jsonFile.close()
        return links

'''
Transforms the raw images into Pillow format
images
'''
def parseImages(imgs):
    PILimages = []
    for img in imgs:
        imageIO = io.BytesIO(img)
        image = Image.open(imageIO).convert('RGB')
        PILimages.append(image)
    return PILimages

def getSoupUrl(url):
    response = requests.get(url)
    return BeautifulSoup(response.text,"html.parser")

def getLinks():
    # To download the whole data set, let's do a for loop through all a tags
    soup = getSoupUrl(BASE_URL)
    links = {}
    lineCount = 1 #variable to track what line you are on
    for one_a_tag in soup.findAll('a'):  #'a' tags are for links
        if lineCount >= 36: #code for text files starts at line 36
            try:
                link = one_a_tag["href"]
            except:
                pass
            if link.startswith(MANGA_URL):
                name = link[32:len(link) - 1]
                links[name] = link
        lineCount +=1
    return links

'''
Iterates trough the link finding all the images and
printing the progress (tqdm)
'''
def getImages(link):
    name = link[32:len(link) - 1]
    soup = getSoupUrl(link)
    imgLinks = soup.find_all("div",{"class": "separator"})
    images = []
    for j in tqdm(range(0,len(imgLinks)), desc = "Downloading chapter: " + str(name)):
        #url = base + "{chapter_name}-{page_number}.jpg".format(chapter_name = chapter_name, page_number = j)
        url = imgLinks[j].next["href"]
        try:
            imgContent = requests.get(url).content
            images.append(imgContent)
        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")
    return images

def _input(message):
    while True:
        try:
            return int(input(message))
        except:
            print('ERROR: Only numbers are allowed\n')
            pass

def main():
    links = readLinks()

    #Query the chapter you wish to download
    search = _input('Please introduce the number of the chapter you want to read\n')
    searchResult = [link for link in links if str(search) in link.split('-')]
    
    if len(searchResult) > 0:
        #Simple menu to select the chapter (it's hard to get the right one just with one number)
        for res in range(0,len(searchResult)):
            print(res," : ",searchResult[res])
        option = _input('Select the chapter by introducing its index\n')
        chapterName = searchResult[int(option)]
        selectedLink = links[chapterName]

        #Downloads the images from that chapter
        imgs = getImages(selectedLink)

        #Transform the images to Pillow format in order to create a pdf
        PILimages = parseImages(imgs)
        del(imgs) #saving memory

        #Tries to create the pdf
        try:
            PILimages[0].save(chapterName+'.pdf', save_all = True, append_images = PILimages)
            print(f'Saved pdf file {chapterName}\n')
        except Exception as e:
            print(f'ERROR Could not save {chapterName} file {e}\n')
        del(PILimages)
    else:
        print(f'ERROR, that chapter number could not be found\n')
    
    input()

main()