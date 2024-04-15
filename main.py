import pandas as pd
from selenium import webdriver
import chromedriver_autoinstaller
import time
from bs4 import BeautifulSoup
from bs4.element import Comment
from selenium.webdriver.common.by import By
import urllib.request
import os
import random
import re

# Install the latest Chromedriver
chromedriver_autoinstaller.install()

driver = webdriver.Chrome()

try:
    os.mkdir("Output")
except:
    pass
os.chdir("Output")


def randNum():
    return random.randint(10, 20)


driver.get("https://investor.sebi.gov.in/moneymatters.html")
time.sleep(randNum())

soup = BeautifulSoup(driver.page_source, 'html.parser')
body = soup.find(attrs={'class': 'portlet-body'})

leftPane = body.find(attrs={'class': 'col-md-4'}).find_all('button')

mainHead = ""
pattern = re.compile('''/[/\\?%*:|"<>]/g''')
for section in leftPane[4:]:
    try:
        source = section.find('a').attrs['href']
    except AttributeError:
        continue

    driver.get(source)
    time.sleep(randNum())

    centerPane = body.find(attrs={'class': 'col-md-8'})

    if section.attrs['class'] == ['mainhead']:
        mainHead = re.sub('''/[/\\?%*:|"<>]/g''', "-", section.text)
        os.mkdir(mainHead)
        with open(f'{mainHead}/content.txt', 'a') as f:
            f.write(centerPane.text)

    elif section.attrs['class'] == ['subhead']:
        subHead = pattern.sub("-", section.text)
        os.makedirs(f'{mainHead}/{subHead}')
        with open(f'{mainHead}/{subHead}/content.txt', 'a') as f:
            f.write(centerPane.text)
    else:
        pass

driver.close()
