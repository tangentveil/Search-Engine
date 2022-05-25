# import string
# import sys
# from sklearn.feature_extraction.text import TfidfVectorizer
# import pandas as pd
# import numpy as np
# import re
# from textblob import TextBlob
# from nltk.stem.porter import PorterStemmer
# from nltk.stem import LancasterStemmer

# def get_similar_articles(q, df):
#   # print("query:", q)
#   # print("cosine similarity: ")

#   # Convert the query become a vector
#   q = [q]
#   q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
#   sim = {}

#   # Calculate the similarity
#   for i in range(10):
#     sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
  
#   # Sort the values 
#   sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)

#   # Print the articles and their similarity values
#   file1 = open('result.txt', 'w+', encoding='utf-8')
#   for k, v in sim_sorted:
#     if v != 0.0:
#       # file1.write("Nilai Similaritas: ")
#       # file1.write(str(v)+'\n'+ '\n')
#       file1.write("Title: " + titles[k] + "\t\t\t\t\t")
#       file1.write("link: " + urls[k] +'\n'+ '\n')
#       file1.write(corpus[k] + '\n' + '\n')
#       # print("Nilai Similaritas: ")
#       # print(str(v)+'\n'+ '\n')
#       print(titles[k])
#       print(urls[k])
#       # print(corpus[k] + '\n' + '\n')


# # Merging all the problems
# corpus = []
# count = 0
# while(count < 1944):
#   count+=1
#   fo1 = open('Problems/problem-'+str(count)+'.txt', encoding='utf-8')
#   docs = fo1.read()
#   corpus.append(docs)

# # Merging all the titles
# titles = []
# fo1_titles = open('problem_titles.txt', encoding='utf-8')
# doc_titles = fo1_titles.read()
# doc_titles = doc_titles.split('\n')
# for title in doc_titles:
#   titles.append(title)
#   corpus.append(title)

# # Merging all the urls
# urls = []
# fo1_urls = open('Problem_urls.txt', encoding='utf-8')
# doc_urls = fo1_urls.read()
# doc_urls = doc_urls.split('\n')
# for url in doc_urls:
#   urls.append(url)
#   corpus.append(url)

# # Text processing
# documents_clean = []
# for d in corpus:
#     # Remove Unicode
#     document_test = re.sub(r'[^\x00-\x7F]+', ' ', d)

#     # Remove Mentions
#     document_test = re.sub(r'@\w+', '', document_test)

#     # Lowercase the document
#     document_test = document_test.lower()

#     # Remove punctuations
#     document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
    
#     # Lowercase the numbers
#     document_test = re.sub(r'[0-9]', '', document_test)

#     #  replace \n with space
#     document_test = re.sub("'\r\n'", r"' '", document_test)

#     # Remove the doubled space
#     document_test = re.sub(r'\s{2,}', ' ', document_test)
#     documents_clean.append(document_test)


# # Instantiate a TfidfVectorizer object
# vectorizer = TfidfVectorizer()

# # It fits the data and transform it as a vector
# X = vectorizer.fit_transform(documents_clean)

# # Convert the X as transposed matrix
# X = X.T.toarray()

# # Create a DataFrame and set the vocabulary as the index
# df = pd.DataFrame(X, index=vectorizer.get_feature_names_out())


# # Add The Query
# queryString = str(sys.argv[1])
# queryString = queryString.lower()
# queryString = TextBlob(queryString)
# queryString = str(queryString.correct())

# stemmer = PorterStemmer()
# queryString = stemmer.stem(queryString)

# # Lanc_stemmer = LancasterStemmer()
# # queryString = Lanc_stemmer.stem(queryString)

# # Call the function
# get_similar_articles(queryString, df)

# /////////////////////////////////////////////////////////////////////////////////

import math
from operator import le
import string
import re
from itertools import count
from pydoc import doc
import sys
import pandas as pd
import numpy as np

from gensim.parsing.preprocessing import remove_stopwords

titles = []
f1_titles = open('./problem_titles.txt', encoding='utf-8')

doc_titles = f1_titles.read()
titles = doc_titles.split('\n')
# print(doc_titles)
# print(titles)


URLs = []
f1_URL = open('./problem_urls.txt', encoding='utf-8')

doc_URL = f1_URL.read()
URLs = doc_URL.split('\n')
# print(doc_titles)
# print(URLs)


keywords = []

sentence = []

for cnt in range(0, 1944):
    f1 = open('Problems/problem-'+str(cnt+1)+'.txt', encoding='utf-8')
    docs = str(f1.read())
    # print(docs)

    # print(docs)

    # print(len(docs))

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
    document_test = re.sub(r'[%s]' % re.escape(
        string.punctuation), ' ', document_test)

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


f1 = open("./Keywords.txt", 'w+')
f1.write('\n'.join(keywords))

# print(keywords)
# print(len(keywords))
# print("\n")

# print((sentence[0]))
# print(len(sentence[1]))

# print(sentence[0].count('example'))


# Calculating TF
TF = []
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
    # print(tf_local)


# print(TF)
# print(len(TF))
# print(len(TF[1]))


# Calculating IDF
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

# print(IDF)
# print(len(IDF))

f1 = open("./IDF.txt", 'w+')
ToAdd = ""

for i in IDF:
    ToAdd += str(i)
    ToAdd += "\n"
f1.write(ToAdd)


# Calculating Importance Matrix (TFIDF Matrix)
Importance_Matrix = []

for i in range(len(TF)):
    Imp_Matrix = []
    Imp_Matrix.append(TF[i][0])
    Imp_Matrix.append(TF[i][1])
    Imp_Matrix.append(TF[i][2] * IDF[TF[i][1]])

    Importance_Matrix.append(Imp_Matrix)


# print((Importance_Matrix))

f1 = open("./TF-IDF.txt", 'w+')
ToAdd = ""

for i in range(len(Importance_Matrix)):
    ToAdd += str(Importance_Matrix[i][0])
    ToAdd += " "
    ToAdd += str(Importance_Matrix[i][1])
    ToAdd += " "
    ToAdd += str(Importance_Matrix[i][2])
    ToAdd += "\n"
f1.write(ToAdd)

# Calculate Magnitude of the vector
Magnitude = []

for i in range(len(sentence)):
    Magnitude.append(0.0)

for i in range(len(Importance_Matrix)):
    Magnitude[Importance_Matrix[i][0]] += Importance_Matrix[i][2] * \
        Importance_Matrix[i][2]

for i in (range(len(Magnitude))):
    Magnitude[i] = math.sqrt(Magnitude[i])


# print(Magnitude)

f1 = open("./Magnitude.txt", 'w+')
ToAdd = ""

for i in Magnitude:
    ToAdd += str(i)
    ToAdd += "\n"
f1.write(ToAdd)


# query string
# query = "Sum of two numbers Magnus tree Given Number diagram integers array string graph"
query = sys.argv[1]

query_keywords = []

filtered_sentence = remove_stopwords(query)
filtered_sentence = filtered_sentence.lower()

filtered_sentence = sorted(filtered_sentence.split(" "))

# print(len(filtered_sentence))

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

# print(query_TF)


query_Importance_Matrix = []

for i in range(len(query_TF)):
    Imp_Matrix = []
    Imp_Matrix.append(query_TF[i][0])
    Imp_Matrix.append(query_TF[i][1])
    Imp_Matrix.append(query_TF[i][2] * IDF[query_TF[i][1]])

    query_Importance_Matrix.append(Imp_Matrix)

# print(query_Importance_Matrix)

query_Magnitude = [0.0]


for i in range(len(query_Importance_Matrix)):
    query_Magnitude[query_Importance_Matrix[i][0]] += query_Importance_Matrix[i][2] * \
        query_Importance_Matrix[i][2]

for i in (range(len(query_Magnitude))):
    query_Magnitude[i] = math.sqrt(query_Magnitude[i])

# print(query_Magnitude)


# similarity

similarity = []

for i in range(len(sentence)):
    sim = []

    sim.append(0.0)
    sim.append(i)
    similarity.append(sim)


for i in range(len(query_Importance_Matrix)):
    toCheckKeyword = query_Importance_Matrix[i][1]
    # print(toCheckKeyword)
    for j in range(len(Importance_Matrix)):
        if Importance_Matrix[j][1] == toCheckKeyword:
            similarity[Importance_Matrix[j][0]
                       ][0] += query_Importance_Matrix[i][2] * Importance_Matrix[j][2]

for i in range(len(sentence)):
    similarity[i][0] = similarity[i][0] / (Magnitude[i]*query_Magnitude[0])

similarity = sorted(similarity, reverse=True)

# print((similarity[0:5]))


for i in (range(len(similarity[0:5]))):
    ques_no = similarity[i][1]
    print(titles[ques_no])
    print(URLs[ques_no])
    f1 = open('Problems/problem-'+str(ques_no+1)+'.txt', encoding='utf-8')
    docs = str(f1.read())

    docs = docs.replace("\\n", " ")
    print(docs[2:100])
    print("\n")