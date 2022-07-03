# [Search-Engine](https://search-engine-v2.herokuapp.com/)
#step 1 : Web Scrapping
**Here is the Python Code:**

```python
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
 ```       
#Step 2: Preparing the Keywords.txt, sentence.txt, idf.txt, tf-df-matrix.txt and Magnitude.txt 
**Python Code :** 

```python
import math
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
# Web App
#Setting Up the Enviornment
```
npm init
```
```
npm i express
```
```
npm i ejs
```
```
npm i stopword
```
#Create app.js
```javascript
const express = require('express');
const ejs = require('ejs');
const PORT = process.env.PORT || 3000;
const app = express();
const path = require('path');
const controller = require('./controllers/controller');

// view engine
app.set('view engine', 'ejs');

// static
app.use(express.static('./public'));

// fire contoller
controller(app);

// port listening
app.listen(PORT, ()=>{
    console.log(`Listening on port : ${PORT}`);
});
```
# Search Engine Algorithm
#controller.js
```javascript
// const { spawn } = require('child_process');
const fs = require('fs');
const console = require('console');
const { removeStopwords, eng, fra } = require('stopword');

module.exports = (app) => {
    app.get('/', (req, res)=>{
        res.render('index');
    });
    
    app.get('/search', (req, res)=>{
        const query = req.query;
        const question = query.question;

        var arr = [];

        var IDF, Imp_Matrix, Importance_Matrix, Magnitude, URLs, cnt, filtered_sentence, keywords, queryString, query_Importance_Matrix, query_Magnitude, query_TF, ques_no, result, sentence, sim, similarity, tf_local, titles, toCheckKeyword, corpus;

        let f1_titles = fs.readFileSync('./problem_titles.txt', {encoding:'utf8', flag:'r'});
        // titles = f1_titles.split('\n');
        titles = f1_titles.toString().replace(/\r\n/g,'\n').split('\n');


        let f1_URLs = fs.readFileSync('./problem_urls.txt', {encoding:'utf8', flag:'r'});
        URLs = f1_URLs.toString().replace(/\r\n/g,'\n').split('\n');


        let f1_keywords = fs.readFileSync('./Keywords.txt', {encoding:'utf8', flag:'r'});
        keywords = f1_keywords.toString().replace(/\r\n/g,'\n').split('\n');


        let f1_sentence = fs.readFileSync('./sentence.txt', {encoding:'utf8', flag:'r'});
        sentence = f1_sentence.split('\n');


        IDF = [];
        let f1_idf = fs.readFileSync('./idf.txt', {encoding:'utf8', flag:'r'});
        IDF_s = f1_idf.toString().replace(/\r\n/g,'\n').split('\n');
        for(let i = 0; i < IDF_s.length; i++){
            result = parseFloat(IDF_s[i]);
            IDF.push(result);
        }

        Importance_Matrix = [];
        let f1_tfidf = fs.readFileSync('./tf-idf.txt', {encoding:'utf8', flag:'r'});
        Importance_Matrix_s = f1_tfidf.toString().replace(/\r\n/g,'\n').split('\n');

        for(let i = 0; i < Importance_Matrix_s.length; i++){
            result = Importance_Matrix_s[i];
            result = result.replace(/\[|\]/g,'').split(',');
            Importance_Matrix.push(result);
        }


        Magnitude = [];
        let f1_magnitude = fs.readFileSync('./Magnitude.txt', {encoding:'utf8', flag:'r'});
        Magnitude_s = f1_magnitude.toString().replace(/\r\n/g,'\n').split('\n');
        for(let i = 0; i < Magnitude_s.length; i++){
            result = parseFloat(Magnitude_s[i]);
            Magnitude.push(result);
        }

        queryString = question;

        queryString = queryString.toLowerCase();
        query_keywords = [];
        queryString = queryString.split(' ');
        filtered_sentence = removeStopwords(queryString);
        filtered_sentence = filtered_sentence.sort();
        query_TF = [];

        function search( arr,  s) {
            var counter = 0;
            for (j = 0; j < arr.length; j++)
                if (s === (arr[j]))
                    counter++;

            return counter;
        }


        for (let j = 0; j < keywords.length; j++){
            cnt = search(filtered_sentence, keywords[j]);

            if (cnt === 0) {
            continue;
            }
            // console.log(keywords[j]);
            tf_local = [];
            tf_local.push(0);
            tf_local.push(j);
            tf_local.push(cnt / filtered_sentence.length);
            query_TF.push(tf_local);
        }



        // console.log(query_TF)
        query_Importance_Matrix = [];

        for (let i = 0; i < query_TF.length; i++){
            Imp_Matrix = [];
            Imp_Matrix.push(query_TF[i][0]);
            Imp_Matrix.push(query_TF[i][1]);
            Imp_Matrix.push(query_TF[i][2] * IDF[query_TF[i][1]]);
            query_Importance_Matrix.push(Imp_Matrix);
        }

        query_Magnitude = [0.0];

        for (let i = 0; i < query_Importance_Matrix.length; i++){
            query_Magnitude[query_Importance_Matrix[i][0]] += query_Importance_Matrix[i][2] * query_Importance_Matrix[i][2];
        }

        for (let i = 0; i < query_Magnitude.length; i++){
            query_Magnitude[i] = Math.sqrt(query_Magnitude[i]);
        }


        if (query_Magnitude[0] === 0.0) {
            console.log("Not Found");
        } else {
            similarity = [];

            for (let i = 0; i < sentence.length; i++) {
            sim = [];
            sim.push(0.0);
            sim.push(i);
            similarity.push(sim);
            }

            for (let i = 0; i < query_Importance_Matrix.length; i++) {
            toCheckKeyword = query_Importance_Matrix[i][1];

            for (let j = 0; j < Importance_Matrix.length; j++) {
                if (Number.parseInt(Importance_Matrix[j][1]) === toCheckKeyword) {
                similarity[Number.parseInt(Importance_Matrix[j][0])][0] += query_Importance_Matrix[i][2] * Number.parseFloat(Importance_Matrix[j][2]);
                }
            }
            }

            for (let i = 0; i < sentence.length; i++) {
            similarity[i][0] = similarity[i][0] / (Magnitude[i] * query_Magnitude[0]);
            }

            similarity = similarity.sort().reverse();

            // copus = [];
            // let f1_corpus = fs.readFileSync('./corpus.txt', {encoding:'utf8', flag:'r'});
            // corpus = f1_corpus.toString().replace(/\r\n/g,'\n').split('\n');
            // corpus = f1_corpus.split('\n');
            // console.log(corpus[0]);

            for (let i = 0; i < similarity.slice(0, 10).length; i++) {
            ques_no = similarity[i][1];
            // console.log(corpus[0][ques_no]);
            // console.log(titles[ques_no]);
            // console.log(URLs[ques_no]);
            arr.push({title:titles[ques_no],url:URLs[ques_no]});
            }
        }

        res.json(arr);
    });
};
```
# Search Engine Web Page
#index.ejs
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Engine</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h1>Search Engine</h1>

    <form>
        <input type="text" name="question" id="question" />
        <input type="submit" id="submit" value="Ake Me:" placeholder="Search..." />
    </form>

    <div class="container">
        
        <div class="loading"></div>

        <div class="question">
            <div class="title"></div>
            <div class="url">
                <a href="" target="_blank"></a>
            </div>
            <div class="question_body"></div>
        </div>
        <div class="question">
            <div class="title"></div>
            <div class="url">
                <a href="" target="_blank"></a>
            </div>
            <div class="question_body"></div>
        </div>
        <div class="question">
            <div class="title"></div>
            <div class="url">
                <a href="" target="_blank"></a>
            </div>
            <div class="question_body"></div>
        </div>
        <div class="question">
            <div class="title"></div>
            <div class="url">
                <a href="" target="_blank"></a>
            </div>
            <div class="question_body"></div>
        </div>
        <div class="question">
            <div class="title"></div>
            <div class="url">
                <a href="" target="_blank"></a>
            </div>
            <div class="question_body"></div>
        </div>
        <div class="question">
            <div class="title"></div>
            <div class="url">
                <a href="" target="_blank"></a>
            </div>
            <div class="question_body"></div>
        </div>
        <div class="question">
            <div class="title"></div>
            <div class="url">
                <a href="" target="_blank"></a>
            </div>
            <div class="question_body"></div>
        </div>
        <div class="question">
            <div class="title"></div>
            <div class="url">
                <a href="" target="_blank"></a>
            </div>
            <div class="question_body"></div>
        </div>
        <div class="question">
            <div class="title"></div>
            <div class="url">
                <a href="" target="_blank"></a>
            </div>
            <div class="question_body"></div>
        </div>
        <div class="question">
            <div class="title"></div>
            <div class="url">
                <a href="" target="_blank"></a>
            </div>
            <div class="question_body"></div>
        </div>
    </div>

</body>
</html>

<script src="/static/script.js"></script>

```
#script.js
```javascript
const form = document.querySelector('form');
const questionElement = form.question;

const question = document.querySelectorAll('.question');
const titles = document.querySelectorAll('.title');
const urls = document.querySelectorAll('.url');
const question_body = document.querySelectorAll('.question_body');
const loading_div = document.querySelector('.loading');

form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const question = questionElement.value;
    for(let i = 0; i < 10; i++){
        titles[i].innerHTML = ``;
        urls[i].innerHTML = ``;
    }

    loading_div.innerHTML = `Loading...`;

    // fetch
    try{
        const res = await fetch(`/search?question=${question}`, { method : "GET", 
        });
        const data = await res.json();

        loading_div.innerHTML = ``;


        for(let i = 0; i < 10; i++){
            titles[i].innerHTML = `<h3>${data[i].title}</h3>`;
            urls[i].innerHTML = `<a href="" target="_blank">${data[i].url}</a>`;
        }

    } catch(error){
        alert(error);
    }
});
```
#style.css
```CSS
body{
    background: #0d1521;
    font-family: tahoma;
    color: #989898;
}

input[type="text"]{
    width: 60%;
    padding: 20px;
    background:#181c22;
    border: 0;
    float: left;
    font-size: 20px;
    color: #989898;
}

#submit{
    padding: 20px;
    width: 30%;
    float: right;
    background: #23282e;
    border: 0;
    box-sizing: border-box;
    color: #fff;
    cursor: pointer;
    font-size: 20px;
}

ul{
    list-style-type: none;
    padding: 0;
    margin: 0;
}

li{
    width: 100%;
    padding: 20px;
    box-sizing: border-box;
    font-family: arial;
    font-size: 20px;
    cursor: pointer;
    letter-spacing: 1px;
}


h1{
    display: flex;
    margin-bottom: 20px;
    justify-content: center;
}

.container{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-top: 8rem;
    padding: 30px 138px;
}

.question{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.loading{
    font-size: 2rem;
}

.url a{
    text-decoration: none;
    color: #989898;
}

.url a:link{
    color: #fff;
}

.url a:active{
    color: rgb(0, 247, 255);
}

.url a:hover{
    color: #fff;
}
```
**After preparing all the files**
**Move the files in their respective folders**
***Ignore the Some of the files which is shown in the screenshot***
![image](https://user-images.githubusercontent.com/59107332/170883742-c2d31256-7774-4be8-b437-f113a01b5711.png)
#.gitignore
```
node_modules/
```
#open pacakge.json and modified
```json
{
  "name": "search-engine",
  "version": "1.0.0",
  "description": "",
  "main": "app.js",
  "scripts": {
    "start": "node app.js"
  },
  "author": "",
  "license": "ISC",
  "dependencies": {
    "ejs": "^3.1.8",
    "express": "^4.18.1",
    "stopword": "^2.0.2"
  }
}
```
# Deploying the Web App
#Make a new git repository and push all the files.
![image](https://user-images.githubusercontent.com/59107332/170885365-9191137d-8a61-4d60-8861-bf5edf3d3569.png)

```
git status
```
```
git add .
```
```
git commit -m 'first commit'
```
```
git push
```
#Setting Up the Heroku
[Click Here](https://devcenter.heroku.com/articles/heroku-cli)
#After Heroku login
```
heroku login
```
#Add the keys
```
heroku add:keys
```
#create heroku app
```
heroku create APPNAME
```
#Push the data to heroku app
```
git push heroku main
```
