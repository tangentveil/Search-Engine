import math
import string
import re
import sys

from gensim.parsing.preprocessing import remove_stopwords

titles = []
f1_titles = open('./problem_titles.txt')
doc_titles = f1_titles.read()
titles = doc_titles.split('\n')


URLs = []
f1_URL = open('./problem_urls.txt')
doc_URL = f1_URL.read()
URLs = doc_URL.split('\n')


keywords = []
f1 = open('./keywords.txt')
docs = f1.read()
docs = docs.split('\n')
for doc in docs:
    keywords.append(doc)


sentence = []
f1 = open('./sentence.txt')
docs = f1.read()
docs = docs.split('\n')
for doc in docs:
    res = doc.replace('"','')
    sentence.append(res)


# IDF
IDF = []
f1 = open('./idf.txt')
docs = f1.read()
docs = docs.split("\n")
for doc in docs:
    res = float(doc)
    IDF.append(res)


# Importance Matrix (TFIDF Matrix)
Importance_Matrix = []
f1 = open('./tf-idf.txt')
docs = f1.read()
docs = docs.split("\n")
for doc in docs:
    res = doc.strip('][').split(', ')
    Importance_Matrix.append(res)


# Magnitude of the vector
Magnitude = []
f1 = open('./Magnitude.txt', encoding='utf-8')
docs = f1.read()
docs = docs.split("\n")
for doc in docs:
    res = float(doc)
    Magnitude.append(res)


# query string
# query = "Sum of two numbers Magnus tree Given Number diagram integers array string graph"
query = sys.argv[1]

query_keywords = []

filtered_sentence = remove_stopwords(query)
filtered_sentence = filtered_sentence.lower()

filtered_sentence = sorted(filtered_sentence.split(" "))


# // Query TF
query_TF = []

for j in range(len(keywords)):
    cnt = (filtered_sentence.count(keywords[j]))
    if cnt == 0:
        continue
    tf_local = []
    tf_local.append(0)
    tf_local.append(j)
    tf_local.append(cnt/len(filtered_sentence))
    query_TF.append(tf_local)


query_Importance_Matrix = []

for i in range(len(query_TF)):
    Imp_Matrix = []
    Imp_Matrix.append(query_TF[i][0])
    Imp_Matrix.append(query_TF[i][1])
    Imp_Matrix.append(query_TF[i][2] * IDF[query_TF[i][1]])

    query_Importance_Matrix.append(Imp_Matrix)

query_Magnitude = [0.0]


for i in range(len(query_Importance_Matrix)):
    query_Magnitude[query_Importance_Matrix[i][0]] += query_Importance_Matrix[i][2] * \
        query_Importance_Matrix[i][2]

for i in (range(len(query_Magnitude))):
    query_Magnitude[i] = math.sqrt(query_Magnitude[i])
    

if(query_Magnitude[0] == 0.0):
        print("Not Found")
else :
    # similarity
    similarity = []
    for i in range(len(sentence)):
        sim = []

        sim.append(0.0)
        sim.append(i)
        similarity.append(sim)

    for i in range(len(query_Importance_Matrix)):
        toCheckKeyword = query_Importance_Matrix[i][1]
        for j in range(len(Importance_Matrix)):
            if int(Importance_Matrix[j][1]) == toCheckKeyword:
                similarity[int(Importance_Matrix[j][0])][0] += query_Importance_Matrix[i][2] * float(Importance_Matrix[j][2])

    for i in range(len(sentence)):
        similarity[i][0] = similarity[i][0] / (Magnitude[i]*query_Magnitude[0])

    similarity = sorted(similarity, reverse=True)


    for i in (range(len(similarity[0:10]))):
        # file1 = open('result.txt', 'a+')
        ques_no = similarity[i][1]
        print(titles[ques_no])
        print(URLs[ques_no])
        # file1.write(titles[ques_no] + '\n')
        # file1.write(URLs[ques_no] + '\n\n')
        # f1 = open('Problems/problem-'+str(ques_no+1)+'.txt', encoding='utf-8')
        # docs = str(f1.read())

        # docs = docs.replace("\\n", " ")
        # print(docs[2:100])
        # print("\n")
        # file1.write(docs[2:100] +'\n')