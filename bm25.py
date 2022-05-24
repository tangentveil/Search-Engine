import string
import sys
from rank_bm25 import BM25Okapi
import re

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

# tokenized_corpus = [doc.split(" ") for doc in corpus]

bm25 = BM25Okapi(documents_clean)
bm25_titles = BM25Okapi(titles)
bm25_urls = BM25Okapi(urls)
# bm25 = BM25Okapi(tokenized_corpus)

# query = str(sys.argv[1])
query = "coins"
# query = 'Snakes and transition from Capitalism to Socialism'
tokenized_query = query.split(" ")

doc_scores = bm25.get_scores(tokenized_query)
doc_scores_titles = bm25_titles.get_scores(tokenized_query)
doc_scores_urls = bm25_urls.get_scores(tokenized_query)

result = bm25.get_top_n(tokenized_query, corpus, n=1)
result_titles = bm25_titles.get_top_n(tokenized_query, titles, n=1)
result_urls = bm25_urls.get_top_n(tokenized_query, urls, n=1)


file1 = open('result.txt', 'w+', encoding='utf-8')
# file1.write("Title: " + titles[k] + "\t\t\t\t\t")
# file1.write("link: " + urls[k] +'\n'+ '\n')
# print(type(result))
file1.write(str(result) + '\n\n')
# print(result)
# print(result_urls)
print(result_titles)

