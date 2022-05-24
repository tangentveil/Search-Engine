import string
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import re
from textblob import TextBlob
from nltk.stem.porter import PorterStemmer
from nltk.stem import LancasterStemmer

def get_similar_articles(q, df):
  # print("query:", q)
  # print("cosine similarity: ")

  # Convert the query become a vector
  q = [q]
  q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
  sim = {}

  # Calculate the similarity
  for i in range(10):
    sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)
  
  # Sort the values 
  sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)

  # Print the articles and their similarity values
  file1 = open('result.txt', 'w+', encoding='utf-8')
  for k, v in sim_sorted:
    if v != 0.0:
      # file1.write("Nilai Similaritas: ")
      # file1.write(str(v)+'\n'+ '\n')
      file1.write("Title: " + titles[k] + "\t\t\t\t\t")
      file1.write("link: " + urls[k] +'\n'+ '\n')
      file1.write(corpus[k] + '\n' + '\n')
      # print("Nilai Similaritas: ")
      # print(str(v)+'\n'+ '\n')
      print(titles[k])
      print(urls[k])
      # print(corpus[k] + '\n' + '\n')


# Merging all the problems
corpus = []
count = 0
while(count < 1944):
  count+=1
  fo1 = open('Problems/problem-'+str(count)+'.txt', encoding='utf-8')
  docs = fo1.read()
  corpus.append(docs)

# Merging all the titles
titles = []
fo1_titles = open('problem_titles.txt', encoding='utf-8')
doc_titles = fo1_titles.read()
doc_titles = doc_titles.split('\n')
for title in doc_titles:
  titles.append(title)
  corpus.append(title)

# Merging all the urls
urls = []
fo1_urls = open('Problem_urls.txt', encoding='utf-8')
doc_urls = fo1_urls.read()
doc_urls = doc_urls.split('\n')
for url in doc_urls:
  urls.append(url)
  corpus.append(url)

# Text processing
documents_clean = []
for d in corpus:
    # Remove Unicode
    document_test = re.sub(r'[^\x00-\x7F]+', ' ', d)

    # Remove Mentions
    document_test = re.sub(r'@\w+', '', document_test)

    # Lowercase the document
    document_test = document_test.lower()

    # Remove punctuations
    document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
    
    # Lowercase the numbers
    document_test = re.sub(r'[0-9]', '', document_test)

    #  replace \n with space
    document_test = re.sub("'\r\n'", r"' '", document_test)

    # Remove the doubled space
    document_test = re.sub(r'\s{2,}', ' ', document_test)
    documents_clean.append(document_test)


# Instantiate a TfidfVectorizer object
vectorizer = TfidfVectorizer()

# It fits the data and transform it as a vector
X = vectorizer.fit_transform(documents_clean)

# Convert the X as transposed matrix
X = X.T.toarray()

# Create a DataFrame and set the vocabulary as the index
df = pd.DataFrame(X, index=vectorizer.get_feature_names_out())


# Add The Query
queryString = str(sys.argv[1])
queryString = queryString.lower()
queryString = TextBlob(queryString)
queryString = str(queryString.correct())

stemmer = PorterStemmer()
queryString = stemmer.stem(queryString)

# Lanc_stemmer = LancasterStemmer()
# queryString = Lanc_stemmer.stem(queryString)

# Call the function
get_similar_articles(queryString, df)