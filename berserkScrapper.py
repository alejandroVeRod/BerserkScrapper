import requests
from bs4 import BeautifulSoup
import os
from urllib.request import urlretrieve
from urllib.request import urlopen
import io
import sys
from PIL import Image
from tqdm import tqdm 

BASE_URL = 'https://berserkonline.com'

def get_url_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text,"html.parser")
def get_manga_links(url):
    # To download the whole data set, let's do a for loop through all a tags
    soup = get_url_soup(url)
    manga_links = []
    line_count = 1 #variable to track what line you are on
    for one_a_tag in soup.findAll('a'):  #'a' tags are for links
        if line_count >= 36: #code for text files starts at line 36
            try:
                link = one_a_tag["href"]
            except:
                pass
            if link.startswith("https://berserkonline.com/manga/berserk-chapter"):
                manga_links.append(link)
        line_count +=1
    return manga_links

def save_image(img_content,file_path):
    try:
        image_file = io.BytesIO(img_content)
        image = Image.open(image_file).convert('RGB')
        with open(file_path,'wb') as f:
            image.save(f,"JPEG",quality = 85)
    except Exception as e:
        print(f"ERROR- Could not save - {e}")

def get_images(manga_links,save_path):
    for i in range(0,len(manga_links)):
        chapter_name = manga_links[i][32:len(manga_links[i]) - 1]
        path = os.path.join(save_path,chapter_name)
        if not os.path.exists(path):
            os.mkdir(path)
        soup = get_url_soup(manga_links[i])
        img_links = soup.find_all("div",{"class": "separator"})
        for j in tqdm(range(0,len(img_links)), desc = "Downloading chapter: " + str(chapter_name)):
            #url = base + "{chapter_name}-{page_number}.jpg".format(chapter_name = chapter_name, page_number = j)
            url = img_links[j].next["href"]
            try:
                img_content = requests.get(url).content
            except Exception as e:
                print(f"ERROR - Could not download {url} - {e}")
            file_path = (str(path) + "/" + str(j) + '.jpg')
            save_image(img_content,file_path)

def main():
    manga_links = get_manga_links(BASE_URL)
    save_path = sys.argv[1]
    if not os.path.exists(save_path):
        print(f"ERROR- {save_path} does not exists")
    get_images(manga_links,save_path)

if __name__ == "__main__":
    main()
