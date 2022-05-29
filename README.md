# Search-Engine
#step 1 : Web Scrapping
**Here is the Python Code:**

```import time
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
 ```       
#Step 2: Preparing the Keywords.txt, sentence.txt, idf.txt, tf-df-matrix.txt and Magnitude.txt 
**Python Code :** 

```import math
import string
import re

from gensim.parsing.preprocessing import remove_stopwords


keywords = []
sentence = []

for cnt in range(0, 1944):
    f1 = open('Problems/problem-'+str(cnt+1)+'.txt', encoding='utf-8')
    docs = str(f1.read())

    # filtered_sentence = remove_stopwords(docs)
    docs = docs.replace("\\n", " ")

    documents_clean = []
    # for :
    # Remove Unicode
    document_test = re.sub(r'[^\x00-\x7F]+', ' ', docs)

    # Remove Mentions
    document_test = re.sub(r'@\w+', ' ', document_test)

    # Lowercase the document
    document_test = document_test.lower()

    # Remove punctuations
    document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)

    # Lowercase the numbers
    document_test = re.sub(r'[0-9]', ' ', document_test)

    # Remove the doubled space
    document_test = re.sub(r'\s{2,}', ' ', document_test)
    documents_clean.append(document_test)

    filtered_sentence = remove_stopwords(documents_clean[0])

    filtered_sentence = sorted(filtered_sentence.split(" "))

    sentence.append(filtered_sentence)

    filtered_sentence = set(filtered_sentence)

    for i in filtered_sentence:
        keywords.append(i)

keywords = sorted(set(keywords))


# writing in the sentence.txt file
f1 = open("./sentence.txt", 'w+')
f1.write(str(sentence))


# Calculating TF and writing in the tf.txt
TF = []
f1 = open('./tf.txt', 'a+', encoding='utf-8')
for i in range(len(sentence)):
    no_of_keywords_local = len(sentence[i])
    # tf_local = []
    for j in range(len(keywords)):
        cnt = (sentence[i].count(keywords[j]))
        if cnt == 0:
            continue
        tf_local = []
        tf_local.append(i)
        tf_local.append(j)
        tf_local.append(cnt/no_of_keywords_local)
        TF.append(tf_local)
        f1.write(str(tf_local) + '\n')


# Calculating IDF and writing in the idf.txt
IDF = []

N = len(sentence)

counts = []
for i in range(len(keywords)):
    counts.append(0)

for i in range(len(TF)):
    counts[TF[i][1]] += 1

# print(counts)
for i in range(len(keywords)):
    IDF.append((1+math.log(N/counts[i])))

f1 = open("./idf.txt", 'a+')
for i in IDF:
  f1.write(str(i) + "\n")


# # Calculating Importance Matrix (TFIDF Matrix) and writing in the tf-idf.txt
Importance_Matrix = []
f1 = open('./tf-idf.txt', 'a+', encoding='utf-8')
for i in range(len(TF)):
    Imp_Matrix = []
    Imp_Matrix.append(TF[i][0])
    Imp_Matrix.append(TF[i][1])
    Imp_Matrix.append(TF[i][2] * IDF[TF[i][1]])

    Importance_Matrix.append(Imp_Matrix)
    f1.write(str(Imp_Matrix) + '\n')


# # Calculate Magnitude of the vector and writing in the Magnitude.txt
Magnitude = []

for i in range(len(sentence)):
    Magnitude.append(0.0)

for i in range(len(Importance_Matrix)):
    Magnitude[Importance_Matrix[i][0]] += Importance_Matrix[i][2] * \
        Importance_Matrix[i][2]

for i in (range(len(Magnitude))):
    Magnitude[i] = math.sqrt(Magnitude[i])


f1 = open("./Magnitude.txt", 'w+')
for i in Magnitude:
  f1.write(str(i) + "\n")
```
