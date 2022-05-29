const fs = require('fs');
const console = require('console');
const { removeStopwords, eng, fra } = require('stopword');

var IDF, Imp_Matrix, Importance_Matrix, Magnitude, URLs, cnt, doc_URL, doc_titles, docs, f1, f1_URL, filtered_sentence, keywords, queryString, query_Importance_Matrix, query_Magnitude, query_TF, query_keywords, ques_no, result, sentence, sim, similarity, tf_local, titles, toCheckKeyword;

let f1_titles = fs.readFileSync('./problem_titles.txt', { encoding: 'utf8', flag: 'r' });
// titles = f1_titles.split('\n');
titles = f1_titles.toString().replace(/\r\n/g, '\n').split('\n');
// console.log(titles.length);
// console.log(typeof(data));


let f1_URLs = fs.readFileSync('./problem_urls.txt', { encoding: 'utf8', flag: 'r' });
URLs = f1_URLs.toString().replace(/\r\n/g, '\n').split('\n');
// URLs = f1_URLs.split('\n');
// console.log(URLs.length);
// console.log(typeof(data));


let f1_keywords = fs.readFileSync('./Keywords.txt', { encoding: 'utf8', flag: 'r' });
keywords = f1_keywords.toString().replace(/\r\n/g, '\n').split('\n');
// console.log(keywords.length);



let f1_sentence = fs.readFileSync('./sentence.txt', { encoding: 'utf8', flag: 'r' });
sentence = f1_sentence.split('\n');


IDF = [];
let f1_idf = fs.readFileSync('./idf.txt', { encoding: 'utf8', flag: 'r' });
IDF_s = f1_idf.toString().replace(/\r\n/g, '\n').split('\n');
for (let i = 0; i < IDF_s.length; i++) {
  result = parseFloat(IDF_s[i]);
  IDF.push(result);
}
// console.log(IDF);
// console.log(IDF.length);


Importance_Matrix = [];
let f1_tfidf = fs.readFileSync('./tf-idf.txt', { encoding: 'utf8', flag: 'r' });
Importance_Matrix_s = f1_tfidf.toString().replace(/\r\n/g, '\n').split('\n');

for (let i = 0; i < Importance_Matrix_s.length; i++) {
  result = Importance_Matrix_s[i];
  result = result.replace(/\[|\]/g, '').split(',');
  Importance_Matrix.push(result);
}


Magnitude = [];
let f1_magnitude = fs.readFileSync('./Magnitude.txt', { encoding: 'utf8', flag: 'r' });
Magnitude_s = f1_magnitude.toString().replace(/\r\n/g, '\n').split('\n');
for (let i = 0; i < Magnitude_s.length; i++) {
  result = parseFloat(Magnitude_s[i]);
  Magnitude.push(result);
}

// queryString = "Sum of two numbers Magnus tree Given Number diagram integers array string graph";
queryString = question;

queryString = queryString.toLowerCase();
query_keywords = [];
queryString = queryString.split(' ');
filtered_sentence = removeStopwords(queryString);
// filtered_sentence = filtered_sentence.toLowerCase;
filtered_sentence = filtered_sentence.sort();
query_TF = [];

function search(arr, s) {
  var counter = 0;
  for (j = 0; j < arr.length; j++)
    if (s === (arr[j]))
      counter++;

  return counter;
}


for (let j = 0; j < keywords.length; j++) {
  // cnt = filtered_sentence.join(' ').split(keywords[j]).length-1;
  // cnt = (filtered_sentence.match(/keywords[j]/g) || length).length;

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

for (let i = 0; i < query_TF.length; i++) {
  Imp_Matrix = [];
  Imp_Matrix.push(query_TF[i][0]);
  Imp_Matrix.push(query_TF[i][1]);
  Imp_Matrix.push(query_TF[i][2] * IDF[query_TF[i][1]]);
  query_Importance_Matrix.push(Imp_Matrix);
}

query_Magnitude = [0.0];

for (let i = 0; i < query_Importance_Matrix.length; i++) {
  query_Magnitude[query_Importance_Matrix[i][0]] += query_Importance_Matrix[i][2] * query_Importance_Matrix[i][2];
}

for (let i = 0; i < query_Magnitude.length; i++) {
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

  for (let i = 0; i < similarity.slice(0, 10).length; i++) {
    ques_no = similarity[i][1];
    console.log(titles[ques_no]);
    console.log(URLs[ques_no]);
    arr.push({ title: titles[ques_no], url: URLs[ques_no] });
  }
}