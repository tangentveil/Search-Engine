# Search-Engine
First step : Web Scrapping
Here is the Code: 

import time
import os
import re

from lib2to3.pgen2 import driver
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://www.codechef.com/tags/problems/prefix-sum")

time.sleep(5)

html = driver.page_source
# print(html)

soup = BeautifulSoup(html, 'html.parser')
all_ques_div = soup.findAll("div", {"class": "problem-tagbox-inner"})

# print(len(all_ques_div))

all_ques = []
for ques in all_ques_div:
    all_ques.append(ques.findAll("div")[0].find("a"))

# print(all_ques[0])

urls = []
title = []
for ques in all_ques:
    urls.append("https://www.codechef.com"+ques['href'])
    title.append(ques.text)

# with open("problem_urls.txt", "w+") as f:
#     f.write('\n'.join(urls))

# with open("problem_titles.txt", "w+") as f:
#     f.write('\n'.join(title))

with open("problem_urls.txt", "a+") as f:
    f.write('\n'.join(urls))

with open("problem_titles.txt", "a+") as f:
    f.write('\n'.join(title))



# Creating New Folder

new_folder = r'Problems'
if not os.path.exists(new_folder):
    os.makedirs(new_folder)

count = 1868
for url in urls:
    driver.get(url)
    count+=1
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    problem_text = soup.find("div", {"class" : "problem-statement"}).get_text()

    # File name with the title.
    with open("Problems/problem-"+str(count)+".txt", "w+", encoding="utf-8") as f:
        txt = problem_text
        # txt = re.sub(r'\n\s*\n', '\n', txt)
        # Adds two blanks between all paragraphs
        txt = re.sub(r'\n\n\n', '\n', txt)
        # Removes the blank lines from the EOF
        txt = re.sub(r'\n*\Z', '', txt)
        f.write(txt)
