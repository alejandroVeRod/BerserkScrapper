# BerserkScrapper
An easy home made scrapper for the berserk manga from berserkonline.com. I do not own any of the rights from the web or the manga, it's just some code pasted in order to get the images and make a pdf per chapter

INSTRUCTIONS:

WINDOWS
--------
Just execute the .exe file then a black window will appear asking for you to put the chapter number you want to read
(from 1 to 364 the latest one), then because the chapter names in berserk are weird it will ask you to select
the one you want, put again the number then wait for the download to finish and the pdf will be in the same path
as the .exe file is!

DEVELOPER
---------
-> Python is needed for the code to execute
-> Make sure you got every library used in this project installed (BeautifulSoup, request, urllib, PILLOW,..)

USAGE:
-> python3 BerserkScrapper.py 
  Then it will ask you for any chapter number you want
  You select the one from the list searched and then it just
  downloads all images and converts them into a pdf, just as simple as that
  
NOTE:
  -> It will generate a manga_links.json file, this is for performance purposes
  if you wish to download more.
you can modify it for any of your needs, I do not own this, its just that I wanted to read the manga in my mobile in pdf

